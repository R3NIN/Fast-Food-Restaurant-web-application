from django.shortcuts import render, redirect
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from Base_App.models import BookTable, AboutUs, Feedback, ItemList, Items

# Cache time in seconds (5 minutes)
CACHE_TTL = 300

class HomeView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        items = Items.objects.select_related('Category').all()
        categories = ItemList.objects.all()
        reviews = Feedback.objects.all()
        
        # Debug output (will show in console)
        print(f"Total items: {items.count()}")
        print(f"Categories: {[c.Category_name for c in categories]}")
        
        return render(request, 'home.html', {
            'items': items, 
            'list': categories, 
            'review': reviews
        })

class AboutView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        data = AboutUs.objects.all()
        return render(request, 'about.html', {'data': data})

class MenuView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        # Get all items with their related category
        items = Items.objects.select_related('Category').all()
        list_items = ItemList.objects.all()
        
        # Debug output
        print(f"Menu View - Total items: {items.count()}")
        print(f"Menu View - Categories: {[c.Category_name for c in list_items]}")
        for item in items:
            print(f"Item: {item.Item_name}, Category: {item.Category.Category_name if item.Category else 'None'}")
        
        return render(request, 'menu.html', {
            'items': items, 
            'list': list_items
        })

class BookTableView(View):
    def get(self, request):
        return render(request, 'book_table.html')
        
    def post(self, request):
        try:
            name = request.POST.get('user_name', '').strip()
            phone = request.POST.get('phone_number', '').strip()
            email = request.POST.get('user_email', '').strip()
            persons = request.POST.get('total_person', '').strip()
            date = request.POST.get('booking_date', '').strip()
            
            if not all([name, phone, email, persons, date]):
                messages.error(request, 'All fields are required.')
                return redirect('Book_Table')
                
            BookTable.objects.create(
                Name=name,
                Phone_number=phone,
                Email=email,
                Total_person=persons,
                Booking_date=date
            )
            messages.success(request, 'Booking successful!')
            return redirect('Book_Table')
            
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
            return redirect('Book_Table')

class FeedbackView(View):
    @method_decorator(cache_page(CACHE_TTL))
    def get(self, request):
        return render(request, 'feedback.html')
        
    def post(self, request):
        try:
            name = request.POST.get('user_name', '').strip()
            description = request.POST.get('description', '').strip()
            rating = request.POST.get('rating', '').strip()
            
            if not all([name, description, rating]):
                messages.error(request, 'Please fill in all required fields.')
                return redirect('Feedback_Form')
                
            # Handle file upload
            feedback_image = request.FILES.get('feedback_image')
            
            # Create the feedback entry
            feedback = Feedback.objects.create(
                Name=name,
                Description=description,
                Rating=rating,
            )
            
            # Save the image if provided
            if feedback_image:
                feedback.Image = feedback_image
                feedback.save()
            
            messages.success(request, 'Thank you for your feedback!')
            return redirect('Feedback_Form')
            
        except Exception as e:
            messages.error(request, f'Error submitting feedback: {str(e)}')
            return redirect('Feedback_Form')