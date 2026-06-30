from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import upload_images


urlpatterns = [

    path(
        "",
        views.home,
        name="home"
    ),
    path(
        "login/",
        views.login_view,
        name="login"
    ),
    path(
        "register/",
        views.register,
        name="register"
    ),
    path(
        "logout/",
        views.logout_view,
        name="logout"
    ),

    path(
        'dashboard',
        views.process_tags,
        name='dashboard'
    ),

    path(
        '',
        views.upload_images,
        name='upload'
    ),

    path(
        'results/',
        views.results,
        name='results'
    ),

    path(
        'export-csv/',
        views.export_csv,
        name='export_csv'
    ),

    path(
        "delete-image/<int:image_id>/",
        views.delete_image,
        name='delete_image'
    ),
    path(
        'export-json/',
        views.export_json,
        name='export_json'
    ),

]
