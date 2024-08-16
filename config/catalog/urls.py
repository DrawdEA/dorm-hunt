from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("dorms/", views.DormsListView.as_view(), name="dorms"),
    path("schools/", views.SchoolsListView.as_view(), name="schools"),
    path("dorm/<int:pk>", views.DormDetailView.as_view(), name="dorm_detail"),
    path("school/<int:pk>", views.SchoolDetailView.as_view(), name="school_detail"),
    path("my-vouches/", views.MyVouchesListView.as_view(), name="my_vouches"),
    path("all-vouches", views.AllVouchesListView.as_view(), name="all_vouches"),
    path('vouch/create/', views.CreateVouch.as_view(), name='create_vouch'),
    path('vouch/<int:pk>/update/', views.UpdateVouch.as_view(), name='update_vouch'),
    path('vouch/<int:pk>/delete/', views.DeleteVouch.as_view(), name='delete_vouch'),
    path('dorm/create/', views.CreateDorm.as_view(), name='create_dorm'),
    path('dorm/<int:pk>/update/', views.UpdateDorm.as_view(), name='update_dorm'),
    path('dorm/<int:pk>/delete/', views.DeleteDorm.as_view(), name='delete_dorm'),
    path('school/create/', views.CreateSchool.as_view(), name='create_school'),
    path('school/<int:pk>/update/', views.UpdateSchool.as_view(), name='update_school'),
    path('school/<int:pk>/delete/', views.DeleteSchool.as_view(), name='delete_school'),
]
