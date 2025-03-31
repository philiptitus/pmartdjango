from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator
from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string

class Category(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=100)
    icon = models.CharField(max_length=10, default="🔧")  # Default icon
    description = models.TextField(blank=True)
    slug = models.SlugField(unique=True)

    def __str__(self):
        return self.name



class Product(models.Model):
    id = models.CharField(max_length=50, primary_key=True)
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    stock = models.IntegerField(default=0)
    rating = models.DecimalField(max_digits=2, decimal_places=1, validators=[MinValueValidator(0), MaxValueValidator(5)])
    reviews = models.IntegerField(default=0)
    is_featured = models.BooleanField(default=False)
    color = models.CharField(max_length=7)  # Store as hex color code

    def __str__(self):
        return self.name
class Feature(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='features')
    text = models.CharField(max_length=255)

    def __str__(self):
        return self.text


class Image(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    url = models.URLField()
    alt_text = models.CharField(max_length=255, blank=True, null=True)

    def __str__(self):
        return self.url

class Contact(models.Model):
    name = models.CharField(max_length=100)
    email = models.EmailField()
    subject = models.CharField(max_length=200)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}"

    def send_acknowledgment_email(self):
        subject = "Thank you for contacting store support!"
        message = f"""
        Hi {self.name},

        Thank you for reaching out concerning my services. I have received your message and will get back to you shortly.

        Here is a copy of your message:
        Subject: {self.subject}
        Message: {self.message}

        Best regards,
        Philip
        """
        html_message = render_to_string('emails/contact_acknowledgment_email.html', {
            'name': self.name,
            'subject': self.subject,
            'message': self.message,
        })
        send_mail(
            subject,
            '',
            settings.DEFAULT_FROM_EMAIL,
            [self.email],
            fail_silently=False,
            html_message=html_message,


        )

class Newsletter(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.email

class Order(models.Model):
    PLATFORM_CHOICES = [
        ('fiverr', 'Fiverr'),
        ('upwork', 'Upwork'),
    ]

    customer_name = models.CharField(max_length=100, blank=True, null=True)
    customer_email = models.EmailField()
    platform = models.CharField(max_length=10, choices=PLATFORM_CHOICES)
    order_details = models.JSONField()  # Store order items as JSON
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    file = models.FileField(upload_to='order_files/', blank=True, null=True)  # Handle attached files
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, default='pending')

    def __str__(self):
        return f"Order by {self.customer_name} - {self.platform}"