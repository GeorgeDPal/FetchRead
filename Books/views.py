import json
import datetime
import requests
from django.conf import settings
from .models import Member, Transaction
from django.shortcuts import render, redirect, get_object_or_404
from .models import Book
from django.urls import reverse
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.contrib import messages
from django.db import IntegrityError
from django.core.validators import validate_email
from django.core.exceptions import ValidationError

def home_page(request):
    return render(request, "base.html")

def add_book(request):
    if request.method == "POST":
        data = request.POST
        title = data.get('title', '').strip()
        authors = data.get('authors', '').strip()
        isbn = data.get('isbn', '').strip()
        publisher = data.get('publisher', '').strip()
        stock = data.get('stock', '').strip()

        if not (title and authors and isbn and publisher and stock):
            messages.error(request, "Please fill in all fields.")
        else:
            try:
                stock = int(stock)
                if stock <= 0:
                    raise ValueError()
            except ValueError:
                messages.error(request, "Stock must be a positive integer.")
            else:
                books_to_create = [
                    Book(title=title, authors=authors, isbn=isbn, publisher=publisher)
                    for _ in range(stock)
                ]

                try:
                    Book.objects.bulk_create(books_to_create)
                    messages.success(request, "You have successfully added new books to the database.")
                except IntegrityError:
                    messages.error(request, "An error occurred. Please try again.")

    return render(request, "add_book.html")

def get_books(request):
    if request.method == "GET":
        # Handle the form submission for searching and importing books from an API
        api_url = settings.API_URLS.get('frappe_library', '')  # Get the API URL from settings
        payload = {
            "title": request.GET.get('title', ''),
            "authors": request.GET.get('authors', ''),
            "isbn": request.GET.get('isbn', ''),
            "publisher": request.GET.get('publisher', ''),
            "page": request.GET.get('page', ''),
        }

        response = requests.get(api_url, params=payload)

        try:
            data = response.json()["message"]
        except:
            data = []

        return render(request, "books_view.html", {"books": data})

    return render(request, "books_view.html")


def add_books(request):
    if request.method == 'GET':
        return redirect("get_books")

    try:
        data = json.load(request)
        books = data.get("books", [])
        stocks = data.get("stocks", [])

        if not stocks:
            messages.error(request, "Please enter the number of books to add to the database.")
            return redirect("get_books")

        books_to_create = []
        for book_info, stock in zip(books, stocks):
            book = book_info.split('\t')
            books_to_create.extend([
                Book(title=book[0], authors=book[1], isbn=book[2], publisher=book[3])
                for _ in range(int(stock))
            ])

        Book.objects.bulk_create(books_to_create)
        messages.success(request, "You have successfully added the books to the database.")
    except Exception as e:
        messages.error(request, f"An error occurred: {str(e)}")

    return redirect("get_books")

def add_member(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        username = data.get('username', '').strip()
        email = data.get('email', '').strip()

        if not (first_name and last_name and username and email):
            messages.error(request, "Please fill in all fields.")
        else:
            try:
                validate_email(email)
            except ValidationError:
                messages.error(request, "Please enter a valid email.")
            else:
                try:
                    Member.objects.create(first_name=first_name, last_name=last_name, username=username, email=email)
                    messages.success(request, "You have successfully added a new member to the database.")
                except IntegrityError:
                    messages.error(request, "Username/email already exists. Please use a different username/email.")

    return render(request, "add_members.html")

def issue_books(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username', '').strip()
        isbn = data.get('isbn', '').strip()

        if not (username and isbn):
            messages.error(request, "Please fill in all fields.")
        else:
            try:
                member = Member.objects.get(username=username)
                book = Book.objects.filter(isbn=isbn, member=None).first()
            except Member.DoesNotExist:
                messages.error(request, "Member does not exist.")
            except Book.DoesNotExist:
                messages.error(request, f"No available books with ISBN {isbn}.")
            else:
                # Check if the member has outstanding debt
                debt = member.calculate_outstanding_debt()
                if debt >= 500:
                    messages.error(request, f"{username}'s outstanding debt is greater than 500. Please return/re-issue books.")
                else:
                    book.issue_to_member(member)
                    messages.success(request, f"{username} has successfully issued the book.")

    return render(request, "issue_books.html")

def return_books(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('username', '').strip()
        book_id = data.get('book_id', '').strip()

        if not (username and book_id):
            messages.error(request, "Please fill in all fields.")
        else:
            try:
                member = Member.objects.get(username=username)
                book = Book.objects.get(pk=book_id, member=member)
            except Member.DoesNotExist:
                messages.error(request, "Member does not exist.")
            except Book.DoesNotExist:
                messages.error(request, "Book does not exist or has not been issued to the member.")
            else:
                amount = book.calculate_return_fees()
                if amount <= 0:
                    messages.success(request, f"{username} has returned the book successfully.")
                messages.info(request, amount)
                book.return_from_member(member)
                messages.success(request, f"{username} has returned the book successfully.")

    return render(request, "return_books.html")

def view_books(request):
    edit_mode = False  # Set edit_mode to False when displaying the list of books

    if request.method == "POST":
        data = request.POST
        title = data.get('title', '').strip()
        authors = data.get('authors', '').strip()

        if not (title or authors):
            messages.error(request, "Please fill in at least one field.")
        else:
            try:
                books = Book.objects.filter(title__icontains=title, authors__icontains=authors).exclude(title='deleted')
            except IntegrityError:
                messages.error(request, "Internal server error. Please try again.")
            else:
                if not books:
                    messages.warning(request, "No books match the query.")

    else:
        # Retrieve all books (or your default logic)
        books = Book.objects.all().exclude(title='deleted')

    return render(request, "books.html", {"books": books, "edit_mode": edit_mode})

def delete_book(request, book_id):
    if request.method == "POST":
        try:
            book = Book.objects.get(pk=book_id)
            book.delete()
            # Use JsonResponse to send a response indicating success
            return JsonResponse({"status": "success"})
        except Book.DoesNotExist:
            # Use JsonResponse to send a response indicating failure
            return JsonResponse({"status": "fail", "message": "Book does not exist."})

    return HttpResponseRedirect(reverse("view_books"))

def view_members(request):
    if request.method == "POST":
        data = request.POST
        first_name = data.get('first_name', '').strip()
        last_name = data.get('last_name', '').strip()
        username = data.get('username', '').strip()

        if not (first_name or last_name or username):
            messages.error(request, "Please fill in at least one field.")
        else:
            try:
                members = Member.objects.filter(
                    first_name__icontains=first_name,
                    last_name__icontains=last_name,
                    username__icontains=username
                ).exclude(username='deleted')
            except IntegrityError:
                messages.error(request, "Internal server error. Please try again.")
            else:
                if not members:
                    messages.warning(request, "No members match the query.")

    members = Member.objects.all().exclude(username='deleted')
    return render(request, "view_members.html", {"members": members})

def edit_book(request, book_id):
    edit_mode = True  # Set edit_mode to True when editing a book

    book = get_object_or_404(Book, pk=book_id)

    if request.method == "POST":
        data = request.POST
        # Update book details directly without using a form
        book.title = data.get('title', '').strip()
        book.authors = data.get('authors', '').strip()
        book.isbn = data.get('isbn', '').strip()
        book.publisher = data.get('publisher', '').strip()
        book.save()
        messages.success(request, "You have successfully updated the book details.")
        # Redirect to the view_books page or another appropriate page
        return redirect("view_books")

   
    return render(request, "books.html", {"book": book, "edit_mode": edit_mode})

def delete_member(request, member_id):
    if request.method == "POST":
        try:
            member = Member.objects.get(pk=member_id)
            member.delete()
            return JsonResponse({"status": "success"})
        except Member.DoesNotExist:
            pass

    return HttpResponseRedirect(reverse("view_members"))

from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from django.db import IntegrityError
from django.core.validators import validate_email
from .models import Member

def edit_member(request, member_id):
    # Get the member object using get_object_or_404
    member = get_object_or_404(Member, pk=member_id)

    if request.method == "POST":
        data = request.POST
        member.first_name = data.get('first_name', '').strip()
        member.last_name = data.get('last_name', '').strip()
        member.username = data.get('username', '').strip()
        member.email = data.get('email', '').strip()

        try:
            validate_email(member.email)
        except ValidationError:
            messages.error(request, "Please enter a valid email.")
        else:
            try:
                member.save()
                messages.success(request, "You have successfully updated the member details.")
                return redirect("view_members")
            except IntegrityError:
                messages.error(request, "Username/email already exists. Please use a different username/email.")

    return render(request, "view_members.html", {"member": member})

def view_transactions(request):
    if request.method == "POST":
        data = request.POST
        username = data.get('member', '').strip()
        isbn = data.get('book', '').strip()
        action = data.get('action')

        transactions = Transaction.objects.all()

        if username:
            transactions = transactions.filter(member__username=username)
        if isbn:
            transactions = transactions.filter(book__isbn=isbn)
        if action:
            transactions = transactions.filter(action=action)

        # Convert transactions to a list of dictionaries
        transactions_data = [
            {
                "member": transaction.member.username,
                "book": transaction.book.isbn,
                "action": transaction.action,
                "date": transaction.date.strftime("%Y-%m-%d %H:%M:%S"),
            }
            for transaction in transactions
        ]

        return JsonResponse({"transactions": transactions_data})

    transactions = Transaction.objects.all()
    return render(request, "view_transactions.html", {"transactions": transactions})