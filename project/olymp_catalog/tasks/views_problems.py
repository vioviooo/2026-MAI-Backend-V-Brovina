# views_problems.py
from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.views.decorators.csrf import csrf_exempt
from django.contrib.admin.views.decorators import staff_member_required
import json
from .models import Problem, Tag, TestCase

@require_http_methods(["GET"])
def problems_list_api(request):
    """Получение всех задач (API)"""
    problems = Problem.objects.all().prefetch_related('tags')

    # Filter 
    difficulty = request.GET.get('difficulty')
    if difficulty:
        problems = problems.filter(difficulty=difficulty)

    tag = request.GET.get('tag')
    if tag:
        problems = problems.filter(tags__name=tag)

    sort = request.GET.get('sort')
    if sort == 'difficulty':
        problems = problems.order_by('difficulty')
    elif sort == '-difficulty':
        problems = problems.order_by('-difficulty')
    
    data = []
    for problem in problems:
        data.append({
            'id': problem.id,
            'title': problem.title,
            'difficulty': problem.difficulty,
            'time_limit': problem.time_limit,
            'memory_limit': problem.memory_limit,
            'tags': [tag.name for tag in problem.tags.all()]
        })
    
    return JsonResponse({
        'status': 'success',
        'count': len(data),
        'data': data
    })

@require_http_methods(["GET"])
def problem_detail_api(request, problem_id):
    """Получение конкретной задачи по ID (API)"""
    try:
        problem = Problem.objects.get(id=problem_id)
        test_cases = list(problem.test_cases.values('input_data', 'expected_output', 'is_sample'))
        
        return JsonResponse({
            'status': 'success',
            'data': {
                'id': problem.id,
                'title': problem.title,
                'statement': problem.statement,
                'difficulty': problem.difficulty,
                'time_limit': problem.time_limit,
                'memory_limit': problem.memory_limit,
                'tags': list(problem.tags.values_list('name', flat=True)),
                'test_cases': [
                    {
                        'input': tc['input_data'],
                        'output': tc['expected_output'],
                        'is_sample': tc['is_sample']
                    }
                    for tc in test_cases
                ]
            }
        })
    except Problem.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Задача не найдена'
        }, status=404)

@staff_member_required # ! only admin can create problems
@require_http_methods(["POST"])
@csrf_exempt
def problem_create(request):
    """Создание новой задачи (только для админов)"""
    try:
        data = json.loads(request.body)
        
        required_fields = ['title', 'statement', 'difficulty']
        for field in required_fields:
            if not data.get(field):
                return JsonResponse({
                    'status': 'error',
                    'message': f'Поле {field} обязательно для заполнения'
                }, status=400)
        
        test_cases_data = data.get('test_cases', [])
        if len(test_cases_data) > 3:
            return JsonResponse({
                'status': 'error',
                'message': 'Максимум 3 тест-кейса на задачу'
            }, status=400)
        
        problem = Problem.objects.create(
            title=data['title'],
            statement=data['statement'],
            difficulty=data.get('difficulty', 'medium'),
            time_limit=float(data.get('time_limit', 1.0)),
            memory_limit=int(data.get('memory_limit', 256))
        )
        
        if data.get('tags'):
            for tag_name in data['tags']:
                tag, _ = Tag.objects.get_or_create(name=tag_name)
                problem.tags.add(tag)
        
        for test in test_cases_data[:3]:
            TestCase.objects.create(
                problem=problem,
                input_data=test.get('input', ''),
                expected_output=test.get('output', ''),
                is_sample=test.get('is_sample', False)
            )
        
        return JsonResponse({
            'status': 'success',
            'message': 'Задача успешно создана',
            'problem_id': problem.id
        }, status=201)
        
    except json.JSONDecodeError:
        return JsonResponse({
            'status': 'error',
            'message': 'Неверный формат JSON'
        }, status=400)
    except Exception as e:
        return JsonResponse({
            'status': 'error',
            'message': str(e)
        }, status=400)

@staff_member_required  # ! only admin can delete problems
@require_http_methods(["POST"])
@csrf_exempt
def problem_delete(request, problem_id):
    """Удаление задачи (только для админов)"""
    try:
        problem = Problem.objects.get(id=problem_id)
        problem_title = problem.title
        problem.delete()
        
        return JsonResponse({
            'status': 'success',
            'message': f'Задача "{problem_title}" успешно удалена'
        })
    except Problem.DoesNotExist:
        return JsonResponse({
            'status': 'error',
            'message': 'Задача не найдена'
        }, status=404)