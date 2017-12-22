from django.shortcuts import render
from django.shortcuts import redirect
from django.utils import timezone
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from .models import *

def index(request):
    return render(request, 'index/index.html', {})

def login(request):
    if request.method == 'POST':
        username = request.POST['Username']
        password = request.POST['Password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            # Redirect to a success page.
            if user.is_superuser:
                return redirect('/admin')
            else:
                return redirect(request.GET.get('next', 'book_info'))
        else:
            # Return an 'invalid login' error message.
            return render(request, 'registration/login.html', {'state': 'not_exist_or_password_error'})
    if request.user.is_authenticated:
        return redirect(request.POST.get('next', 'book_info'))
    else:
        return render(request, 'registration/login.html',
                      {'state': 'login_first' if request.GET.get('next', '') else None})

def logout(request):
    auth_logout(request)
    return redirect('index')

@login_required(login_url='/login/')
def book_info(request):
    user = request.user
    if user.is_superuser:
        return redirect('/admin')
    search_item = request.GET.get('Search')
    page = 'book_info'
    if search_item is None:
        books = Book.objects.all()
    else:
        books = Book.objects.filter(name__contains=search_item) \
                                                    or Book.objects.filter(author__contains=search_item) \
                                                    or Book.objects.filter(publishing__contains=search_item) \
                                                    or Book.objects.filter(category__contains=search_item)
    return render(request, 'interface/book_list.html', {'books': books, 'user': user, 'page': page})

@login_required(login_url='/login/')
def user_info(request):
    user = request.user
    page = 'user_info'
    borrowed = Borrow.objects.filter(reader=user.profile, is_returned=False).order_by('-date_borrow')
    history = Borrow.objects.filter(reader=user.profile).order_by('-date_borrow')
    return render(request, 'interface/user_info.html',
                  {'borrowed': borrowed, 'history': history, 'user': user, 'page': page})
