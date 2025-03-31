from django.core.management.base import BaseCommand
from ecommerce.models import Category, Product
import json
import os
import re

class Command(BaseCommand):
    help = 'Import categories and products from data.ts file'

    def clean_json_str(self, json_str):
        """Clean up JSON string to make it valid"""
        # Remove trailing commas in arrays and objects
        json_str = re.sub(r',(\s*[}\]])', r'\1', json_str)
        # Remove any remaining trailing commas
        json_str = re.sub(r',(\s*$)', '', json_str)
        return json_str

    def extract_ts_data(self, file_path, data_type):
        """Extract data from TypeScript file using regex"""
        self.stdout.write(f'Reading {data_type} from {file_path}...')
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            
            if data_type == 'categories':
                pattern = r'export const categories = \[(.*?)\];'
            else:  # products
                pattern = r'export const products = \[(.*?)\];'
            
            match = re.search(pattern, content, re.DOTALL)
            if match:
                data_str = match.group(1)
                self.stdout.write(f'Found {data_type} data in file')
                
                # Remove any TypeScript-specific syntax
                data_str = re.sub(r'//.*?\n|/\*.*?\*/', '', data_str, flags=re.DOTALL)  # Remove comments
                self.stdout.write('Removed comments')
                
                # Clean up arrays and objects
                data_str = self.clean_json_str(data_str)
                data_str = re.sub(r'`([^`]*)`', r'"\1"', data_str)  # Convert template literals
                self.stdout.write('Cleaned up arrays and objects')
                
                # Convert TypeScript object to valid JSON
                data_str = re.sub(r'(\w+):', r'"\1":', data_str)  # Quote property names
                self.stdout.write('Converted property names')
                
                try:
                    data = json.loads(f'[{data_str}]')
                    self.stdout.write(self.style.SUCCESS(f'Successfully parsed {len(data)} {data_type}'))
                    return data
                except json.JSONDecodeError as e:
                    self.stdout.write(self.style.ERROR(f'Error parsing {data_type}: {str(e)}'))
                    self.stdout.write(self.style.ERROR(f'Problematic JSON: [{data_str}]'))
                    return []
            else:
                self.stdout.write(self.style.ERROR(f'No {data_type} found in file'))
                return []

    def handle(self, *args, **kwargs):
        # Get the path to data.ts file
        current_dir = os.path.dirname(os.path.abspath(__file__))
        workspace_root = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(current_dir))))
        data_ts_path = os.path.join(workspace_root, 'lib', 'data.ts')
        
        self.stdout.write(f'Looking for data.ts at: {data_ts_path}')
        
        if not os.path.exists(data_ts_path):
            self.stdout.write(self.style.ERROR(f'data.ts not found at {data_ts_path}'))
            return
            
        # Clear existing data
        self.stdout.write('Clearing existing data...')
        Category.objects.all().delete()
        Product.objects.all().delete()
        
        # Import categories
        categories_data = self.extract_ts_data(data_ts_path, 'categories')
        if not categories_data:
            self.stdout.write(self.style.ERROR('No categories data found'))
            return
            
        categories_map = {}  # Map category IDs to objects
        for category_data in categories_data:
            try:
                self.stdout.write(f'Creating category: {category_data}')
                category = Category.objects.create(
                    id=category_data['id'],
                    name=category_data['name'],
                    icon=category_data['icon'],
                    description=category_data['description'],
                    slug=category_data['slug']
                )
                categories_map[category.id] = category
                self.stdout.write(self.style.SUCCESS(f'Created category: {category.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating category {category_data.get("name", "unknown")}: {str(e)}'))

        # Import products
        products_data = self.extract_ts_data(data_ts_path, 'products')
        if not products_data:
            self.stdout.write(self.style.ERROR('No products data found'))
            return
            
        for product_data in products_data:
            try:
                self.stdout.write(f'Creating product: {product_data}')
                category_id = product_data.pop('category')
                category = categories_map.get(category_id)
                if not category:
                    self.stdout.write(self.style.ERROR(f'Category {category_id} not found for product {product_data.get("name", "unknown")}'))
                    continue
                
                # Convert isFeatured to is_featured if present
                if 'isFeatured' in product_data:
                    product_data['is_featured'] = product_data.pop('isFeatured')
                
                # Convert lists to JSON strings
                if 'features' in product_data:
                    product_data['features'] = json.dumps(product_data['features'])
                if 'images' in product_data:
                    product_data['images'] = json.dumps(product_data['images'])
                
                # Remove any fields not in the model
                product_data.pop('isNew', None)
                product_data.pop('originalPrice', None)
                
                product = Product.objects.create(
                    category=category,
                    **product_data
                )
                self.stdout.write(self.style.SUCCESS(f'Created product: {product.name}'))
            except Exception as e:
                self.stdout.write(self.style.ERROR(f'Error creating product {product_data.get("name", "unknown")}: {str(e)}'))

        # Print final counts
        category_count = Category.objects.count()
        product_count = Product.objects.count()
        self.stdout.write(self.style.SUCCESS(f'Import complete. Categories: {category_count}, Products: {product_count}')) 