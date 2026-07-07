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

    path('protected/', views.protected_api, name='protected_api'),
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
        'dashboard/',
        views.process_tags,
        name='dashboard'
    ),

    path(
        'upload/',
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
# JWT APIs
    path('api/login/', views.login_api, name='login_api'),
    path('api/upload/', views.upload_api, name='upload_api'),
    path('api/results/', views.results_api, name='results_api'),
    path('api/detect/',views.detect_api,name='detect_api'),
    path('api/profile/', views.profile_api, name='profile_api'),
    path('api/logout/', views.logout_api, name='logout_api'),

]
