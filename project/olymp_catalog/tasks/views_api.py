from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from .models import UserProblemStatus, Problem
from django.utils import timezone

# профиль
@require_http_methods(["GET", "POST"])
def profile_api(request):
    if request.method == "GET":
        if request.user.is_authenticated:
            return JsonResponse({
                "status": "success",
                "data": {
                    "username": request.user.username,
                    "email": request.user.email,
                    "date_joined": request.user.date_joined.isoformat(),
                }
            })
        return JsonResponse({"status": "error", "message": "Не авторизован"}, status=401)
    
    elif request.method == "POST":
        if not request.user.is_authenticated:
            return JsonResponse({"status": "error", "message": "Не авторизован"}, status=401)
        
        # заглушка для обновления профиля
        return JsonResponse({
            "status": "success",
            "message": "Профиль обновлён (заглушка)"
        })

# список категорий
@require_http_methods(["GET"])
def categories_api(request):
    categories = [
        {"id": 1, "name": "Базовые задачи", "slug": "basic"},
        {"id": 2, "name": "Сортировки", "slug": "sorting"},
        {"id": 3, "name": "Динамическое программирование", "slug": "dp"},
        {"id": 4, "name": "Графы", "slug": "graphs"},
    ]
    return JsonResponse({"status": "success", "data": categories})

# категория с задачами
@require_http_methods(["GET"])
def category_detail_api(request, category_slug):
    problems = [
        {"id": 1, "title": f"Задача в категории {category_slug}", "difficulty": "easy"}
    ]
    return JsonResponse({
        "status": "success",
        "category": category_slug,
        "problems": problems
    })

@require_http_methods(["POST"])
@login_required
def update_problem_status_api(request, problem_id):
    """Сохраняет статус задачи для пользователя (Решено / Хочу решить)"""
    status = request.POST.get('status')
    
    if status not in ['solved', 'want']:
        return JsonResponse({
            "status": "error",
            "message": "Некорректный статус"
        }, status=400)
    
    try:
        problem = Problem.objects.get(id=problem_id)
    except Problem.DoesNotExist:
        return JsonResponse({
            "status": "error",
            "message": "Задача не найдена"
        }, status=404)
    
    # Создаём или обновляем статус
    user_status, created = UserProblemStatus.objects.update_or_create(
        user=request.user,
        problem=problem,
        defaults={'status': status}
    )
    
    return JsonResponse({
        "status": "success",
        "message": f"Задача {problem.title} {'решена' if status == 'solved' else 'добавлена в Хочу решить'}"
    })

@require_http_methods(["GET"])
@login_required
def get_user_solved_api(request):
    """Получает список решённых задач пользователя"""
    user_statuses = UserProblemStatus.objects.filter(
        user=request.user,
        status='solved'
    ).select_related('problem')
    
    problems = [{
        'id': us.problem.id,
        'title': us.problem.title,
        'difficulty': us.problem.difficulty
    } for us in user_statuses]
    
    return JsonResponse({"status": "success", "problems": problems})

@require_http_methods(["GET"])
@login_required
def get_user_want_api(request):
    """Получает список задач 'Хочу решить' пользователя"""
    user_statuses = UserProblemStatus.objects.filter(
        user=request.user,
        status='want'
    ).select_related('problem')
    
    problems = [{
        'id': us.problem.id,
        'title': us.problem.title,
        'difficulty': us.problem.difficulty
    } for us in user_statuses]
    
    return JsonResponse({"status": "success", "problems": problems})