from django.urls import path

from . import views

urlpatterns = [
    path("login/", views.login_view, name="login"),
    path("logout/", views.logout_view, name="logout"),
    path("register/", views.register, name="register"),
    path('cv-admin/', views.cv_admin, name='cv_admin'),
    path('cv-admin/edit/<str:model_name>/<uuid:record_id>/', views.cv_edit, name='cv_edit'),
    path('cv_admin/create/<str:model_name>/', views.cv_create, name='cv_create'),
    path('cv-admin/restore/<str:model_name>/<uuid:record_id>/', views.cv_restore, name='cv_restore'),
    path('cv-admin/delete/<str:model_name>/<uuid:record_id>/', views.cv_delete, name='cv_delete'),
]