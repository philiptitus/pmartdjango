from django.core.management.base import BaseCommand
from ecommerce.models import Product

class Command(BaseCommand):
    help = 'List all product names in the database.'

    def handle(self, *args, **options):
        for product in Product.objects.all():
            self.stdout.write(product.name)
