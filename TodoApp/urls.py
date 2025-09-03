from django.urls import path
from .views import register_view, login_view, dashboard_view, landing_page_view, create_task_view, task_delete_view, task_update_view, logout_view, logout_confirm_view

urlpatterns = [
    path('', landing_page_view, name='landingpage'),
    path('register/', register_view, name='register'),
    path('login/', login_view, name='login'),
    path('dashboard/', dashboard_view, name='dashboard'),
    path('task/create/', create_task_view, name='task_create'),
    path('task/delete/<int:task_id>/', task_delete_view, name='task_delete'),
    path('task/update/<int:task_id>/', task_update_view, name='task_update'),
    path('logout/', logout_view, name='logout'),
    path('logout/confirm/', logout_confirm_view, name='logout_confirm'),

]