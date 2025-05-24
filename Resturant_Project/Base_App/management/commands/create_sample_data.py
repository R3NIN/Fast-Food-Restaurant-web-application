import os
import tempfile
import time
from urllib.request import urlretrieve
from io import BytesIO
import requests
from django.core.management.base import BaseCommand
from django.core.files import File
from django.conf import settings
from Base_App.models import ItemList, Items

def download_sample_image(url, filename, max_retries=3, timeout=30):
    """
    Download an image from a URL with retry logic.
    
    Args:
        url: The URL of the image to download
        filename: The filename to use when saving
        max_retries: Maximum number of retry attempts
        timeout: Timeout in seconds for the request
    
    Returns:
        tuple: (file_content, filename) if successful, (None, None) if failed
    """
    for attempt in range(max_retries):
        try:
            response = requests.get(url, stream=True, timeout=timeout)
            response.raise_for_status()
            return BytesIO(response.content), filename
        except requests.exceptions.RequestException as e:
            print(f"Attempt {attempt + 1} failed for {url}: {e}")
            if attempt == max_retries - 1:  # Last attempt
                print(f"Error downloading image after {max_retries} attempts: {e}")
                return None, None
            time.sleep(1)  # Wait before retrying
    return None, None

def create_sample_data():
    # Ensure media directory exists
    os.makedirs(os.path.join(settings.MEDIA_ROOT, 'items'), exist_ok=True)
    
    # Sample images from reliable sources
    sample_images = {
        # Appetizers
        'Bruschetta': 'https://images.pexels.com/photos/6941012/pexels-photo-6941012.jpeg',
        'Spring Rolls': 'https://images.pexels.com/photos/1279330/pexels-photo-1279330.jpeg',
        'Garlic Bread': 'https://images.pexels.com/photos/90894/pexels-photo-90894.jpeg',
        'Mozzarella Sticks': 'https://images.pexels.com/photos/1893555/pexels-photo-1893555.jpeg',
        'Onion Rings': 'https://images.pexels.com/photos/1907228/pexels-photo-1907228.jpeg',
        
        # Main Course
        'Margherita Pizza': 'https://images.pexels.com/photos/1146760/pexels-photo-1146760.jpeg',
        'Grilled Salmon': 'https://images.pexels.com/photos/164716/pexels-photo-164716.jpeg',
        'Chicken Alfredo': 'https://images.pexels.com/photos/11853261/pexels-photo-11853261.jpeg',
        'Beef Burger': 'https://images.pexels.com/photos/1633578/pexels-photo-1633578.jpeg',
        'Vegetable Stir Fry': 'https://images.pexels.com/photos/725990/pexels-photo-725990.jpeg',
        'Grilled Chicken': 'https://images.pexels.com/photos/6210876/pexels-photo-6210876.jpeg',
        'Beef Steak': 'https://images.pexels.com/photos/3535395/pexels-photo-3535395.jpeg',
        'Pasta Carbonara': 'https://images.pexels.com/photos/1437267/pexels-photo-1437267.jpeg',
        'Vegetable Lasagna': 'https://images.pexels.com/photos/4079522/pexels-photo-4079522.jpeg',
        'Fish and Chips': 'https://images.pexels.com/photos/1907229/pexels-photo-1907229.jpeg',
        'Chicken Tikka Masala': 'https://images.pexels.com/photos/2474661/pexels-photo-2474661.jpeg',
        'Beef Tacos': 'https://images.pexels.com/photos/8448323/pexels-photo-8448323.jpeg',
        'Mushroom Risotto': 'https://images.pexels.com/photos/3763847/pexels-photo-3763847.jpeg',
        
        # Desserts
        'Chocolate Lava Cake': 'https://images.pexels.com/photos/45202/brownie-dessert-cake-sweet-45202.jpeg',
        'Cheesecake': 'https://images.pexels.com/photos/132694/pexels-photo-132694.jpeg',
        'Tiramisu': 'https://images.pexels.com/photos/2144112/pexels-photo-2144112.jpeg',
        'Apple Pie': 'https://images.pexels.com/photos/291528/pexels-photo-291528.jpeg',
        'Ice Cream Sundae': 'https://images.pexels.com/photos/1625235/pexels-photo-1625235.jpeg',
        
        # Drinks
        'Iced Tea': 'https://images.pexels.com/photos/5946667/pexels-photo-5946667.jpeg',
        'Mojito': 'https://images.pexels.com/photos/1267702/pexels-photo-1267702.jpeg',
        'Fresh Orange Juice': 'https://images.pexels.com/photos/96974/pexels-photo-96974.jpeg',
        'Cappuccino': 'https://images.pexels.com/photos/302899/pexels-photo-302899.jpeg',
        'Mango Lassi': 'https://images.pexels.com/photos/1346347/pexels-photo-1346347.jpeg',  # Updated image URL
    }
    
    # Create categories
    categories = [
        'Appetizers',
        'Main Course',  # Note the space to match the category name exactly
        'Desserts',
        'Drinks'
    ]
    
    created_categories = {}
    for cat_name in categories:
        # First delete any existing category to avoid duplicates
        ItemList.objects.filter(Category_name=cat_name).delete()
        # Create new category
        cat = ItemList.objects.create(Category_name=cat_name)
        created_categories[cat_name] = cat
        print(f"Created category: {cat_name} (ID: {cat.id})")
    
    # Verify categories were created
    print("\nAll categories in database:")
    for cat in ItemList.objects.all():
        print(f"- {cat.Category_name} (ID: {cat.id})")
    
    # Sample menu items with categories and descriptions
    menu_items = [
        # Appetizers (5 items)
        {
            'name': 'Bruschetta',
            'description': 'Toasted bread topped with tomatoes, garlic, and fresh basil',
            'price': 8,
            'category': 'Appetizers',
            'image_url': sample_images['Bruschetta']
        },
        {
            'name': 'Spring Rolls',
            'description': 'Crispy vegetable spring rolls with sweet chili sauce',
            'price': 7,
            'category': 'Appetizers',
            'image_url': sample_images['Spring Rolls']
        },
        {
            'name': 'Garlic Bread',
            'description': 'Toasted bread with garlic butter and herbs',
            'price': 5,
            'category': 'Appetizers',
            'image_url': sample_images['Garlic Bread']
        },
        {
            'name': 'Mozzarella Sticks',
            'description': 'Breaded mozzarella sticks with marinara sauce',
            'price': 9,
            'category': 'Appetizers',
            'image_url': sample_images['Mozzarella Sticks']
        },
        {
            'name': 'Onion Rings',
            'description': 'Crispy fried onion rings with dipping sauce',
            'price': 6,
            'category': 'Appetizers',
            'image_url': sample_images['Onion Rings']
        },
        
        # Main Course (15 items)
        {
            'name': 'Margherita Pizza',
            'description': 'Classic pizza with tomato sauce and mozzarella',
            'price': 12,
            'category': 'Main Course',
            'image_url': sample_images['Margherita Pizza']
        },
        {
            'name': 'Grilled Salmon',
            'description': 'Fresh salmon fillet with lemon butter sauce',
            'price': 18,
            'category': 'Main Course',
            'image_url': sample_images['Grilled Salmon']
        },
        {
            'name': 'Chicken Alfredo',
            'description': 'Fettuccine pasta with creamy Alfredo sauce and grilled chicken',
            'price': 16,
            'category': 'Main Course',
            'image_url': sample_images['Chicken Alfredo']
        },
        {
            'name': 'Beef Burger',
            'description': 'Juicy beef patty with cheese, lettuce, and special sauce',
            'price': 14,
            'category': 'Main Course',
            'image_url': sample_images['Beef Burger']
        },
        {
            'name': 'Vegetable Stir Fry',
            'description': 'Fresh seasonal vegetables stir-fried in a savory sauce',
            'price': 13,
            'category': 'Main Course',
            'image_url': sample_images['Vegetable Stir Fry']
        },
        {
            'name': 'Grilled Chicken',
            'description': 'Tender grilled chicken breast with herbs and spices',
            'price': 15,
            'category': 'Main Course',
            'image_url': sample_images['Grilled Chicken']
        },
        {
            'name': 'Beef Steak',
            'description': 'Juicy ribeye steak cooked to perfection with roasted vegetables',
            'price': 24,
            'category': 'Main Course',
            'image_url': sample_images['Beef Steak']
        },
        {
            'name': 'Pasta Carbonara',
            'description': 'Classic Italian pasta with creamy egg sauce, pancetta, and parmesan',
            'price': 16,
            'category': 'Main Course',
            'image_url': sample_images['Pasta Carbonara']
        },
        {
            'name': 'Vegetable Lasagna',
            'description': 'Layers of pasta, fresh vegetables, and melted cheese in tomato sauce',
            'price': 14,
            'category': 'Main Course',
            'image_url': sample_images['Vegetable Lasagna']
        },
        {
            'name': 'Fish and Chips',
            'description': 'Beer-battered cod fillet with crispy fries and tartar sauce',
            'price': 17,
            'category': 'Main Course',
            'image_url': sample_images['Fish and Chips']
        },
        {
            'name': 'Chicken Tikka Masala',
            'description': 'Tender chicken in a rich and creamy tomato-based curry sauce',
            'price': 16,
            'category': 'Main Course',
            'image_url': sample_images['Chicken Tikka Masala']
        },
        {
            'name': 'Beef Tacos',
            'description': 'Three soft corn tortillas filled with seasoned beef, lettuce, and cheese',
            'price': 14,
            'category': 'Main Course',
            'image_url': sample_images['Beef Tacos']
        },
        {
            'name': 'Mushroom Risotto',
            'description': 'Creamy arborio rice with wild mushrooms and parmesan cheese',
            'price': 16,
            'category': 'Main Course',
            'image_url': sample_images['Mushroom Risotto']
        },
        
        # Desserts (5 items)
        {
            'name': 'Chocolate Lava Cake',
            'description': 'Warm chocolate cake with a molten center, served with vanilla ice cream',
            'price': 8,
            'category': 'Desserts',
            'image_url': sample_images['Chocolate Lava Cake']
        },
        {
            'name': 'Cheesecake',
            'description': 'Classic New York style cheesecake with strawberry topping',
            'price': 7,
            'category': 'Desserts',
            'image_url': sample_images['Cheesecake']
        },
        {
            'name': 'Tiramisu',
            'description': 'Italian coffee-flavored dessert with layers of coffee-soaked ladyfingers',
            'price': 9,
            'category': 'Desserts',
            'image_url': sample_images['Tiramisu']
        },
        {
            'name': 'Apple Pie',
            'description': 'Homemade apple pie with a flaky crust and vanilla ice cream',
            'price': 7,
            'category': 'Desserts',
            'image_url': sample_images['Apple Pie']
        },
        {
            'name': 'Ice Cream Sundae',
            'description': 'Vanilla ice cream with chocolate sauce, whipped cream, and a cherry on top',
            'price': 6,
            'category': 'Desserts',
            'image_url': sample_images['Ice Cream Sundae']
        },
        
        # Drinks (5 items)
        {
            'name': 'Iced Tea',
            'description': 'Refreshing iced tea with lemon',
            'price': 3,
            'category': 'Drinks',
            'image_url': sample_images['Iced Tea']
        },
        {
            'name': 'Mojito',
            'description': 'Classic mojito with fresh mint, lime, and soda',
            'price': 8,
            'category': 'Drinks',
            'image_url': sample_images['Mojito']
        },
        {
            'name': 'Fresh Orange Juice',
            'description': 'Freshly squeezed orange juice',
            'price': 5,
            'category': 'Drinks',
            'image_url': sample_images['Fresh Orange Juice']
        },
        {
            'name': 'Cappuccino',
            'description': 'Espresso with steamed milk and foam',
            'price': 4,
            'category': 'Drinks',
            'image_url': sample_images['Cappuccino']
        },
        {
            'name': 'Mango Lassi',
            'description': 'Refreshing yogurt-based drink with mango',
            'price': 5,
            'category': 'Drinks',
            'image_url': sample_images['Mango Lassi']
        }
    ]
    
    for item_data in menu_items:
        try:
            # Get the category object
            category_name = item_data['category']
            category = created_categories.get(category_name)
            if not category:
                print(f"Warning: Category '{category_name}' not found for {item_data['name']}")
                continue
                
            # Create or update the item
            item, created = Items.objects.update_or_create(
                Item_name=item_data['name'],
                defaults={
                    'description': item_data['description'],
                    'Price': item_data['price'],
                    'Category': category,
                }
            )
            
            # Download and set the image if URL is provided
            if item_data['image_url']:
                image_content, filename = download_sample_image(
                    item_data['image_url'], 
                    f"{item_data['name'].lower().replace(' ', '_')}.jpg"
                )
                if image_content and filename:
                    item.Image.save(filename, image_content, save=True)
                    print(f"Added image for: {item_data['name']}")
                else:
                    print(f"Failed to download image for: {item_data['name']}")
            
            print(f"{'Created' if created else 'Updated'} menu item: {item_data['name']} (Category: {category_name})")
            
        except Exception as e:
            print(f"Error processing {item_data.get('name', 'unknown')}: {str(e)}")
        
class Command(BaseCommand):
    help = 'Creates sample data for the restaurant app'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data...')
        create_sample_data()
        self.stdout.write('Sample data created successfully!')
