from django.core.management.base import BaseCommand
from ecommerce.models import Product

class Command(BaseCommand):
    help = "Set the images and features fields of all products to empty lists"

    def handle(self, *args, **kwargs):
        # Fetch all products
        products = Product.objects.all()
        self.stdout.write(f"Found {products.count()} products. Updating images and features fields...")

        # Update the images and features fields for each product
        for product in products:
            product.images = []  # Set images to an empty list
            product.features = []  # Set features to an empty list
            product.save()
            self.stdout.write(f"Updated product: {product.name} (ID: {product.id})")

        self.stdout.write(self.style.SUCCESS("Successfully updated all product images and features to empty lists."))