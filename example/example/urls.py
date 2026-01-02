"""
URL configuration for example project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
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

from core import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("index", views.index),
    path("write", views.write_json),
    path("file", views.write_file),
    path("form", views.write_form),
    path("json_form_data", views.json_form_data),
    path("form_form_data", views.form_form_data),

    path("form_old", views.write_form_old),
    path("file_old", views.write_file_old),
    path("json_old", views.write_json_old),

    path("post_first_fail", views.invalid_data_after_post),
    path("data_first_fail", views.invalid_post_after_data),
]
