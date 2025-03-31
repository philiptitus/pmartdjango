from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from rest_framework.pagination import PageNumberPagination

from django.template.loader import render_to_string
from .models import Category, Product, Contact, Newsletter, Order
from .serializers import (
    CategorySerializer, ProductSerializer, ContactSerializer,
    NewsletterSerializer, OrderSerializer
)
from rest_framework.views import APIView


class ProductPagination(PageNumberPagination):
    page_size = 10  # Number of products per page
    page_size_query_param = 'page_size'  # Allow the client to specify the page size
    max_page_size = 100  # Maximum number of products per page


class CategoryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    lookup_field = 'slug'  # Use 'slug' instead of 'id' for category lookup_field = 'slug'  # Use 'slug' instead of the default 'id'

    @action(detail=True, methods=['get'], url_path='details')
    def get_category_details(self, request, pk=None):
        """Fetch category details by slug."""
        try:
            category = Category.objects.get(slug=pk)
            serializer = self.get_serializer(category)
            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)


class ProductViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.filter(stock__gt=0)  # Exclude out-of-stock products
    serializer_class = ProductSerializer
    pagination_class = ProductPagination  # Enable pagination

    def get_queryset(self):
        queryset = Product.objects.filter(stock__gt=0)  # Exclude out-of-stock products
        categories = self.request.query_params.get('categories', None)  # Get the 'categories' query parameter
        sort = self.request.query_params.get('sort', 'featured')  # Get the 'sort' query parameter, default to 'featured'
        search_query = self.request.query_params.get('search', None)  # Get the 'search' query parameter

        # Apply search filter
        if search_query:
            queryset = queryset.filter(
                name__icontains=search_query
            ) | queryset.filter(
                description__icontains=search_query
            )

        # Filter by categories
        if categories:
            category_ids = categories.split(",")  # Split the comma-separated string into a list
            queryset = queryset.filter(category__id__in=category_ids)  # Filter products by category IDs

        # Apply sorting
        if sort == 'price-low-high':
            queryset = queryset.order_by('price')  # Sort by price (ascending)
        elif sort == 'price-high-low':
            queryset = queryset.order_by('-price')  # Sort by price (descending)
        elif sort == 'rating':
            queryset = queryset.order_by('-rating')  # Sort by rating (descending)
        elif sort == 'newest':
            queryset = queryset.order_by('-created_at')  # Sort by newest (descending)
        else:
            queryset = queryset.order_by('-is_featured')  # Default to featured products first

        # Limit search results to 5 if a search query is provided
        if search_query:
            return queryset[:5]

        return queryset
    
    @action(detail=False, methods=['get'])
    def featured(self, request):
        featured_products = self.queryset.filter(is_featured=True)
        serializer = self.get_serializer(featured_products, many=True)
        return Response(serializer.data)
    
class ContactViewSet(viewsets.ModelViewSet):
    queryset = Contact.objects.all()
    serializer_class = ContactSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Send acknowledgment email to the user
        contact = serializer.instance
        contact.send_acknowledgment_email()

        # Send notification email to admin
        subject = f"New Contact Form Submission: {contact.subject}"
        html_message = render_to_string('emails/contact_notification_email.html', {
            'name': contact.name,
            'email': contact.email,
            'subject': contact.subject,
            'message': contact.message,
        })
        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
            html_message=html_message,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

class NewsletterViewSet(viewsets.ModelViewSet):
    queryset = Newsletter.objects.all()
    serializer_class = NewsletterSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)

        # Send welcome email
        subscriber = serializer.instance
        subject = "Welcome to Our Newsletter!"
        message = f"""
        Thank you for subscribing to our newsletter!
        We're excited to keep you updated with our latest products and offers.
        """
        
        send_mail(
            subject,
            message,
            settings.DEFAULT_FROM_EMAIL,
            [subscriber.email],
            fail_silently=False,
        )

        return Response(serializer.data, status=status.HTTP_201_CREATED)

from django.core.mail import send_mail
from django.conf import settings



import json







class OrderViewSet(viewsets.ModelViewSet):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer

    def create(self, request, *args, **kwargs):
        # Extract data from the request
        platform = request.data.get('platform')
        order_details_raw = request.data.get('orderDetails')  # Get the JSON object as a string
        file = request.FILES.get('file')  # Handle attached file

        # Parse the orderDetails JSON object
        try:
            order_details = json.loads(order_details_raw)  # Parse the JSON string into a Python dictionary
        except (TypeError, ValueError):
            return Response(
                {"error": "Invalid orderDetails format. Must be a valid JSON object."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Extract fields from the parsed orderDetails
        items = order_details.get('items', [])
        total_amount = order_details.get('total')
        customer_email = order_details.get('email')
        customer_name = order_details.get('name', 'Anonymous')  # Default to 'Anonymous' if not provided

        # Validate required fields
        if not customer_email or not platform or not items or not total_amount:
            return Response(
                {"error": "Missing required fields: customer_email, platform, items, or total_amount"},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Validate and process each item in the order
        for item in items:
            product_id = item.get('id')
            quantity = item.get('quantity')

            # Validate product existence
            try:
                product = Product.objects.get(id=product_id)
            except Product.DoesNotExist:
                return Response(
                    {"error": f"Product with ID {product_id} does not exist."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validate stock availability
            if product.stock < quantity:
                return Response(
                    {"error": f"Not enough stock for product '{product.name}'. Available: {product.stock}, Requested: {quantity}."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

            # Validate minimum and maximum order quantities
            if quantity <= 0:
                return Response(
                    {"error": f"Invalid quantity for product '{product.name}'. Quantity must be greater than 0."},
                    status=status.HTTP_400_BAD_REQUEST,
                )
            MAX_ORDER_QUANTITY = 10
            if quantity > MAX_ORDER_QUANTITY:
                return Response(
                    {"error": f"Cannot order more than {MAX_ORDER_QUANTITY} units of '{product.name}'."},
                    status=status.HTTP_400_BAD_REQUEST,
                )

        # Deduct stock for each item
        for item in items:
            product_id = item.get('id')
            quantity = item.get('quantity')
            product = Product.objects.get(id=product_id)
            product.stock -= quantity
            product.save()

        # Save the order to the database
        order = Order.objects.create(
            platform=platform,
            customer_email=customer_email,
            customer_name=customer_name,
            order_details=items,  # Save the items as JSON
            total_amount=total_amount,
            file=file,
        )

        # Prepare platform-specific message
        platform_message = (
            "I will be sending you a personalized offer from Fiverr within the next 12 hours. "
            "You can accept it so I can start your project."
            if platform == "fiverr"
            else "I will be sending you a personalized proposal from Upwork within the next 12 hours. "
                 "You can accept it so I can start your project."
        )

        # Render client email
        client_email_html = render_to_string('emails/client_email_template.html', {
            'customer_name': customer_name,
            'platform': platform,
            'total_amount': total_amount,
            'items': items,
            'platform_message': platform_message,
        })

        # Render admin email
        admin_email_html = render_to_string('emails/admin_email_template.html', {
            'customer_name': customer_name,
            'customer_email': customer_email,
            'platform': platform,
            'total_amount': total_amount,
            'items': items,
        })

        # Send email to the customer
        send_mail(
            subject="Thank you for your order!",
            message="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[customer_email],
            fail_silently=False,
            html_message=client_email_html,
        )

        # Send email to the admin
        send_mail(
            subject=f"New Order Received from {customer_name}",
            message="",
            from_email=settings.DEFAULT_FROM_EMAIL,
            recipient_list=[settings.DEFAULT_FROM_EMAIL],
            fail_silently=False,
            html_message=admin_email_html,
        )

        # Serialize and return the response
        serializer = self.get_serializer(order)
        return Response(serializer.data, status=status.HTTP_201_CREATED)



class ProductsByCategoryView(APIView):
    def get(self, request, slug):
        """Fetch products by category slug."""
        print(f"DEBUG: Entered ProductsByCategoryView with slug={slug}")  # Debugging: Check the slug value

        try:
            category = Category.objects.get(slug=slug)
            print(f"DEBUG: Found category: {category}")  # Debugging: Check if the category is found

            products = Product.objects.filter(category=category)
            print(f"DEBUG: Found products: {products}")  # Debugging: Check the products queryset

            serializer = ProductSerializer(products, many=True)
            print(f"DEBUG: Serialized products: {serializer.data}")  # Debugging: Check serialized data

            return Response(serializer.data, status=status.HTTP_200_OK)
        except Category.DoesNotExist:
            print(f"DEBUG: Category with slug '{slug}' does not exist")  # Debugging: Category not found
            return Response({"error": "Category not found"}, status=status.HTTP_404_NOT_FOUND)