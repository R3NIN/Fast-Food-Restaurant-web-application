from django.contrib import admin
from Base_App.models import *

class ItemsAdmin(admin.ModelAdmin):
    list_display = ('Item_name', 'Price', 'Category', 'display_image')
    list_filter = ('Category',)
    search_fields = ('Item_name', 'description')
    
    def display_image(self, obj):
        if obj.Image:
            return f'<img src="{obj.Image.url}" width="50" height="50" />'
        return "No Image"
    display_image.allow_tags = True
    display_image.short_description = 'Image Preview'

class ItemListAdmin(admin.ModelAdmin):
    list_display = ('Category_name', 'item_count')
    
    def item_count(self, obj):
        return obj.Name.count()
    item_count.short_description = 'Number of Items'

class BookTableAdmin(admin.ModelAdmin):
    list_display = ('Name', 'Phone_number', 'Email', 'Total_person', 'Booking_date')
    list_filter = ('Booking_date',)
    search_fields = ('Name', 'Email')

class FeedbackAdmin(admin.ModelAdmin):
    list_display = ('User_name', 'Rating', 'display_image')
    list_filter = ('Rating',)
    
    def display_image(self, obj):
        if obj.Image:
            return f'<img src="{obj.Image.url}" width="50" height="50" />'
        return "No Image"
    display_image.allow_tags = True
    display_image.short_description = 'Image Preview'

# Register your models here.
admin.site.register(ItemList, ItemListAdmin)
admin.site.register(Items, ItemsAdmin)
admin.site.register(AboutUs)
admin.site.register(Feedback, FeedbackAdmin)
admin.site.register(BookTable, BookTableAdmin)
