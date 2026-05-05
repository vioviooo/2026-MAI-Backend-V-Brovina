"""
URL configuration for olymp_catalog project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from tasks.views_api import (
    profile_api, problems_list_api, problem_detail_api,
    categories_api, category_detail_api, update_problem_status_api
)
from tasks.views_web import (
    index, problems_list, problem_detail, category_list,
    category_detail, profile, my_solved, my_want
)

urlpatterns = [
    # API endpoints
    path('api/profile/', profile_api, name='api_profile'),
    path('api/problems/', problems_list_api, name='api_problems'),
    path('api/problems/<int:problem_id>/', problem_detail_api, name='api_problem_detail'),
    path('api/categories/', categories_api, name='api_categories'),
    path('api/categories/<slug:category_slug>/', category_detail_api, name='api_category_detail'),
    path('api/problems/<int:problem_id>/status/', update_problem_status_api, name='api_update_status'),
    
    # Web endpoints
    path('web/', index, name='web_index'),
    path('web/problems/', problems_list, name='web_problems'),
    path('web/problems/<int:problem_id>/', problem_detail, name='web_problem_detail'),
    path('web/categories/', category_list, name='web_categories'),
    path('web/categories/<slug:category_slug>/', category_detail, name='web_category_detail'),
    path('web/profile/', profile, name='web_profile'),
    path('web/my/solved/', my_solved, name='web_my_solved'),
    path('web/my/want/', my_want, name='web_my_want'),
    
    # Admin
    path('admin/', admin.site.urls),
]