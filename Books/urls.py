from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home_page'),  # Use base.html as the template for home_page
    path('add_book/', views.add_book, name='add_book'),
    path('get_books/', views.get_books, name='get_books'),
    path('add_books/', views.add_books, name='add_books'),
    path('add_member/', views.add_member, name='add_member'),
    path('issue_books/', views.issue_books, name='issue_books'),
    path('return_books/', views.return_books, name='return_books'),
    path('view_books/', views.view_books, name='view_books'),
    path('delete_book/<int:book_id>/', views.delete_book, name='delete_book'),
    path('edit_book/<int:book_id>/', views.edit_book, name='edit_book'),
    path('delete_member/<int:member_id>/', views.delete_member, name='delete_member'),
    path('edit_member/<int:member_id>/', views.edit_member, name='edit_member'),
    path('view_transactions/', views.view_transactions, name='view_transactions'),
    path('view_members/', views.view_members, name='view_members'),

]
