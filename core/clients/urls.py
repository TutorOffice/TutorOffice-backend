from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import (
    TokenObtainPairView, TokenRefreshView
)
from django.contrib.auth.views import (
    PasswordResetDoneView, PasswordResetCompleteView
)

register_router = routers.DefaultRouter()
register_router.register('register', RegisterViewSet, basename='register')


urlpatterns = [
    path('', include(register_router.urls)),
    path('login/',
         TokenObtainPairView.as_view(),
         name='login'),
    path('refresh/',
         TokenRefreshView.as_view(),
         name='refresh'),
    path('auth/user-activate/<str:token>/',
         ActivateUserView.as_view(),
         name='activate'),
    path('profile/',
         ProfileViewSet.as_view({'get': 'retrieve',
                                 'patch': 'update'}),
         name='profile',),
    path('password-reset/', CustomPasswordResetView.as_view(),
         name='password-reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(),
         name='password-reset-done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(),
         name='password-reset-confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(),
         name='password-reset-complete'),
    path('subjects/',
         SubjectsView.as_view(),
         name='subjects'),
    path('teacher/subjects/',
         UserSubjectViewSet.as_view({'get': 'list', 'put': 'update',
                                     'post': 'create'}),
         name='teacher-subjects'),
    path('teacher/students/',
         TeacherStudentsViewSet.as_view({'get': 'list',
                                        'post': 'create'}),
         name='teacher-students',
         ),
    path('teacher/student/<int:pk>/',
         TeacherStudentsViewSet.as_view({'delete': 'destroy',
                                         'patch': 'partial_update'}),
         name='teacher-student'),
    path('relate/student/<int:pk>/',
         RelateUnrelateStudentView.as_view(),
         name='relate'),
    path('confirm/<token>',
         ConfirmView.as_view(),
         name='confirm'),
]
