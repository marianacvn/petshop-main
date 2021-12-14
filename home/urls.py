from django.urls import path
from . import views

app_name = 'home'

urlpatterns = [
    path('', views.HomeView.as_view(), name='contact'),
    path('products/', views.ProductsView.as_view(), name='products'),
    path('services/', views.ServicesView.as_view(), name='services'),
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('register/client/', views.ClientCreateView.as_view(), name='register-client'),
    path('update/client/<int:pk>', views.ClientUpdateView.as_view(), name='update-client'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('register/schedule/', views.ScheduleRegisterView.as_view(), name='register-schedule'),

    # Endpoints
    path('product/create/', views.product_create, name='register-product'),
    path('product/update/<int:index>', views.product_update, name='update-product'),
    path('product/filter/', views.product_filter, name='filter-product'),
    path('product/detail/', views.product_detail, name='detail-product'),
    path('product/delete/', views.product_delete, name='delete-product'),

    path('service/create/', views.product_create, name='register-service'),
    path('service/update/<int:index>', views.product_update, name='update-service'),
    path('service/filter/', views.product_filter, name='filter-service'),
    path('service/detail/', views.product_detail, name='detail-service'),
    path('service/delete/', views.product_delete, name='delete-service'),

    path('schedule/all/', views.view_schedule, name='all-schedules')

]
