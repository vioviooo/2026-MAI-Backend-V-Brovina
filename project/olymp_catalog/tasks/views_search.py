from django.http import JsonResponse
from django.views.decorators.http import require_http_methods
from django.db.models import Q
from .models import Problem, Contest

@require_http_methods(["GET"])
def search(request):
    """Поиск по задачам и соревнованиям"""
    query = request.GET.get('q', '').strip()
    
    if not query:
        return JsonResponse({
            'status': 'error',
            'message': 'Параметр q обязателен'
        }, status=400)
    
    # Поиск в задачах (по названию и условию)
    problems = Problem.objects.filter(
        Q(title__icontains=query) | Q(statement__icontains=query)
    ).values('id', 'title', 'difficulty')
 
    return JsonResponse({
        'status': 'success',
        'query': query,
        'problems': list(problems),
        'total': problems.count()
    })