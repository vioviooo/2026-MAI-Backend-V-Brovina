from django.contrib import admin
from django.urls import path
from tasks.views_web import index, problems_list_web, problem_detail_web, category_list, category_detail, profile, my_solved, my_want, register_view, login_view, logout_view
from tasks.views_search import search
from tasks.views_api import profile_api, categories_api, category_detail_api, update_problem_status_api
from tasks.views_problems import problems_list_api, problem_detail_api, problem_create, problem_delete
from tasks.views_api import get_user_solved_api, get_user_want_api

urlpatterns = [
    # API endpoints (return JSON)
    path('api/profile/', profile_api, name='api_profile'),
    path('api/problems/', problems_list_api, name='api_problems'),
    path('api/problems/<int:problem_id>/', problem_detail_api, name='api_problem_detail'),
    path('api/problems/create/', problem_create, name='api_problem_create'),
    path('api/problems/<int:problem_id>/delete/', problem_delete, name='api_problem_delete'),
    path('api/search/', search, name='api_search'),
    path('api/problems/<int:problem_id>/delete/', problem_delete, name='api_problem_delete'),
    path('api/categories/', categories_api, name='api_categories'),
    path('api/categories/<slug:category_slug>/', category_detail_api, name='api_category_detail'),
    path('api/problems/<int:problem_id>/status/', update_problem_status_api, name='api_update_status'),
    path('api/user/solved/', get_user_solved_api, name='api_user_solved'),
    path('api/user/want/', get_user_want_api, name='api_user_want'),

    # Web endpoints (return HTML)
    path('web/', index, name='web_index'),
    path('web/problems/', problems_list_web, name='web_problems'),
    path('web/problems/<int:problem_id>/', problem_detail_web, name='web_problem_detail'),
    path('web/categories/', category_list, name='web_categories'),
    path('web/categories/<slug:category_slug>/', category_detail, name='web_category_detail'),
    path('web/profile/', profile, name='web_profile'),
    path('web/my/solved/', my_solved, name='web_my_solved'),
    path('web/my/want/', my_want, name='web_my_want'),

    # Auth endpoints
    path('web/register/', register_view, name='web_register'),
    path('web/login/', login_view, name='web_login'),
    path('web/logout/', logout_view, name='web_logout'),
    
    # Admin
    path('admin/', admin.site.urls),
]