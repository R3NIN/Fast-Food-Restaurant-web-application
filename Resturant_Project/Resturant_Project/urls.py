"""
URL configuration for Resturant_Project project.
"""
from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from Base_App.views import (
    HomeView,
    BookTableView,
    MenuView,
    AboutView,
    FeedbackView
)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', HomeView.as_view(), name="Home"),
    path('book_table/', BookTableView.as_view(), name='Book_Table'),
    path('menu/', MenuView.as_view(), name='Menu'),
    path('about/', AboutView.as_view(), name='About'),
    path('feedback/', FeedbackView.as_view(), name='Feedback_Form'),
]

# Serve media files in development only
if settings.DEBUG:
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)