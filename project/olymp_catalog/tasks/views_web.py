from django.shortcuts import render
from django.views.decorators.http import require_http_methods
from django.contrib.auth.decorators import login_required

@require_http_methods(["GET"])
def index(request):
    return render(request, 'web/index.html', {
        'page_title': 'Главная'
    })

@require_http_methods(["GET"])
def problems_list(request):
    return render(request, 'web/problems.html', {
        'page_title': 'Каталог задач'
    })

@require_http_methods(["GET"])
def problem_detail(request, problem_id):
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