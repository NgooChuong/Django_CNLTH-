from django.urls import path, re_path, include
from rest_framework import routers
from courses import views

r = routers.DefaultRouter()
r.register('categories', views.CategoryViewSet, 'categories')
r.register('courses', views.CourseViewSet, 'courses')
r.register('lesson',views.LessonViewSet,'lessons')
r.register('users',views.UserViewSet,'user')

urlpatterns = [
    path('', include(r.urls)),
]