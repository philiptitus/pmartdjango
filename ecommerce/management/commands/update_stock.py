from django.core.management.base import BaseCommand
from ecommerce.models import Product

class Command(BaseCommand):
    help = 'Update the stock for all products to exactly 10'

    def handle(self, *args, **kwargs):
        updated_count = Product.objects.update(stock=10)
        update_featured = Product.objects.update(is_featured=False)
        self.stdout.write(self.style.SUCCESS(f'Successfully updated stock for {updated_count} products.'))