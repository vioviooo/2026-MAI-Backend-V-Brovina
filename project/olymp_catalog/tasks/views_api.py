from django.views.decorators.http import require_http_methods
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required

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

# список задач
@require_http_methods(["GET"])
def problems_list_api(request):
    category = request.GET.get('category')
    difficulty = request.GET.get('difficulty')
    
    problems_data = [
        {
            "id": 1,
            "title": "A + B",
            "description": "Найти сумму двух чисел",
            "category": "basic",
            "difficulty": "easy",
            "time_limit": 1.0,
            "memory_limit": 256,
        },
        {
            "id": 2,
            "title": "Сортировка пузырьком",
            "description": "Реализовать сортировку пузырьком",
            "category": "sorting",
            "difficulty": "medium",
            "time_limit": 2.0,
            "memory_limit": 256,
        },
        {
            "id": 3,
            "title": "Задача о рюкзаке",
            "description": "Найти оптимальный набор предметов",
            "category": "dp",
            "difficulty": "hard",
            "time_limit": 2.0,
            "memory_limit": 512,
        }
    ]
    
    if category:
        problems_data = [p for p in problems_data if p["category"] == category]
    if difficulty:
        problems_data = [p for p in problems_data if p["difficulty"] == difficulty]
    
    return JsonResponse({
        "status": "success",
        "count": len(problems_data),
        "data": problems_data
    })

# конкретная задача
@require_http_methods(["GET"])
def problem_detail_api(request, problem_id):
    problem_data = {
        "id": problem_id,
        "title": "A + B" if problem_id == 1 else "Сложная задача",
        "description": "Найти сумму двух чисел" if problem_id == 1 else "Решить сложную задачу",
        "category": "basic",
        "difficulty": "easy",
        "test_cases": [
            {"input": "1 2", "output": "3", "is_sample": True},
            {"input": "5 7", "output": "12", "is_sample": False},
        ],
        "hints": [
            "Используйте стандартный ввод/вывод",
            "Обратите внимание на типы данных"
        ]
    }
    return JsonResponse({"status": "success", "data": problem_data})

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

# добавить задачу в статус
@require_http_methods(["POST"])
@login_required
def update_problem_status_api(request, problem_id):
    status = request.POST.get('status')
    return JsonResponse({
        "status": "success",
        "message": f"Задача {problem_id} обновлена на статус: {status} (заглушка)"
    })
