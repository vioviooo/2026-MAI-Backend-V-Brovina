# views_web.py
from django.shortcuts import render, redirect
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.models import User
from django.contrib import messages

@require_http_methods(["GET"])
def index(request):
    return render(request, 'web/index.html', {
        'page_title': 'Главная'
    })

@require_http_methods(["GET"])
def problems_list_web(request):  # Renamed from problems_list
    return render(request, 'web/problems.html', {
        'page_title': 'Каталог задач'
    })

@require_http_methods(["GET"])
def problem_detail_web(request, problem_id):  # Renamed from problem_detail
    return render(request, 'web/problem_detail.html', {
        'page_title': 'Задача',
        'problem_id': problem_id
    })


@require_http_methods(["GET"])
@login_required
def profile(request):
    return render(request, 'web/profile.html', {
        'page_title': 'Личный кабинет'
    })

@require_http_methods(["GET"])
@login_required
def my_solved(request):
    return render(request, 'web/my_solved.html', {
        'page_title': 'Решённые задачи'
    })

@require_http_methods(["GET"])
@login_required
def my_want(request):
    return render(request, 'web/my_want.html', {
        'page_title': 'Хочу решить'
    })

@require_http_methods(["GET"])
def category_list(request):
    return render(request, 'web/categories.html', {
        'page_title': 'Категории'
    })

@require_http_methods(["GET"])
def category_detail(request, category_slug):
    return render(request, 'web/category_detail.html', {
        'page_title': 'Категория',
        'category_slug': category_slug
    })


@require_http_methods(["GET", "POST"])
def register_view(request):
    """Регистрация нового пользователя"""
    if request.user.is_authenticated:
        return redirect('/web/')
    
    if request.method == "POST":
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password_confirm = request.POST.get('password_confirm')
        
        # Проверки
        if not username or not password:
            messages.error(request, 'Имя пользователя и пароль обязательны')
            return render(request, 'web/register.html')
        
        if password != password_confirm:
            messages.error(request, 'Пароли не совпадают')
            return render(request, 'web/register.html')
        
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Пользователь с таким именем уже существует')
            return render(request, 'web/register.html')
        
        if email and User.objects.filter(email=email).exists():
            messages.error(request, 'Пользователь с таким email уже существует')
            return render(request, 'web/register.html')
        
        # Создаём пользователя
        user = User.objects.create_user(
            username=username,
            email=email,
            password=password
        )
        
        # Автоматически логиним после регистрации
        login(request, user)
        messages.success(request, f'Добро пожаловать, {username}!')
        return redirect('/web/')
    
    return render(request, 'web/register.html')


@require_http_methods(["GET", "POST"])
def login_view(request):
    """Вход пользователя"""
    if request.user.is_authenticated:
        return redirect('/web/')
    
    if request.method == "POST":
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            login(request, user)
            messages.success(request, f'С возвращением, {username}!')
            
            # Перенаправляем на страницу, откуда пришли
            next_url = request.GET.get('next', '/web/')
            return redirect(next_url)
        else:
            messages.error(request, 'Неверное имя пользователя или пароль')
    
    return render(request, 'web/login.html')


@require_http_methods(["POST"])
def logout_view(request):
    """Выход пользователя"""
    logout(request)
    messages.success(request, 'Вы вышли из системы')
    return redirect('/web/')