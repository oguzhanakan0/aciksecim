"""
URL configuration for src project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from election.views import (
    index, 
    get_city, 
    get_district,
    search_box, 
    get_or_create_box, 
    get_all_boxes, 
    get_all_reports,
    create_vote_report,
    get_vote_report,
    verify_vote_report,
)

urlpatterns = [
    path('', index),
    path('sandik/', get_city),
    path('sandik/<str:city>/', get_district, name='get-district'),
    path('sandik/<str:city>/<str:district>/', search_box, name='search-box'),
    path('sandik/<str:city>/<str:district>/<int:box_number>/', get_or_create_box, name='get-or-create-box'),
    path('sandik/<str:city>/<str:district>/sandik-listesi/', get_all_boxes, name='get-all-boxes'),
    path('sandik/<str:city>/<str:district>/tutanak-listesi/', get_all_reports, name='get-all-reports'),
    path('tutanak/<str:pk>/', get_vote_report),
    path('actions/create-vote-report/', create_vote_report, name='create-vote-report'),
    path('actions/verify-vote-report/', verify_vote_report, name='verify-vote-report'),
    path('admin/', admin.site.urls),
]
