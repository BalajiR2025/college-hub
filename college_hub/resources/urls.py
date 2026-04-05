from django.urls import path
from . import views
urlpatterns = [
    path('dashboard/', views.DashboardView.as_view(), name='dashboard'),
    path('resources/', views.ResourceListView.as_view(), name='resource_list'),
    path('resources/<int:pk>/', views.ResourceDetailView.as_view(), name='resource_detail'),
    path('resources/<int:pk>/download/', views.download_resource, name='download'),
    path('resources/<int:pk>/rate/', views.rate_resource, name='rate'),
    path('resources/<int:pk>/report/', views.report_resource, name='report'),
    path('resources/<int:pk>/toggle-important/', views.toggle_important, name='toggle_important'),
    path('requests/', views.RequestListView.as_view(), name='requests'),
    path('requests/new/', views.RequestCreateView.as_view(), name='request_create'),
]