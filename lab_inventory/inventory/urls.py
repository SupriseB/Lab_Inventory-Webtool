from django.urls import path
from . import views

urlpatterns = [
    # Category CRUD
    path('categories/', views.CategoryListView.as_view(), name='category-list'),
    path('categories/new/', views.CategoryCreateView.as_view(), name='category-create'),
    path('categories/<int:pk>/edit/', views.CategoryUpdateView.as_view(), name='category-update'),
    path('categories/<int:pk>/delete/', views.CategoryDeleteView.as_view(), name='category-delete'),

    # Item CRUD
    path('items/', views.ItemListView.as_view(), name='item-list'),
    path('items/new/', views.ItemCreateView.as_view(), name='item-create'),
    path('items/<int:pk>/edit/', views.ItemUpdateView.as_view(), name='item-update'),
    path('items/<int:pk>/delete/', views.ItemDeleteView.as_view(), name='item-delete'),

    #Dashboard
    path('dashboard/', views.dashboard, name='dashboard'),

    #Data Exportation
    #Full stock
    path("export/csv/", views.export_csv, name="export_csv"),
    path("export/pdf/", views.export_pdf, name="export_pdf"),
    #Low stock
    path("export/lowstock/csv/", views.export_lowstock_csv, name="export_lowstock_csv"),
    path("export/lowstock/pdf/", views.export_lowstock_pdf, name="export_lowstock_pdf"),
]
