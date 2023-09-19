from django.contrib import admin
from .models import Member, Book, Transaction

@admin.register(Member)
class MemberAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'username', 'email']

@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ['id', 'title', 'authors', 'isbn', 'publisher', 'member']

@admin.register(Transaction)
class TransactionAdmin(admin.ModelAdmin):
    list_display = ['id', 'member', 'book', 'date', 'action', 'fees']
