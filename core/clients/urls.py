from django.urls import path, include
from rest_framework import routers
from .views import *
from rest_framework_simplejwt.views import TokenRefreshView
from django.contrib.auth.views import (
    PasswordResetDoneView, PasswordResetCompleteView, PasswordChangeView, PasswordChangeDoneView
)

app_name = 'clients'

router = routers.DefaultRouter()
router.register('register',
                RegisterViewSet,
                basename='register')
router.register('student/teachers',
                StudentTeachersViewSet,
                basename='student_teachers')


urlpatterns = [
    path('', include(router.urls)),
    path('login/',
         LoginView.as_view(),
         name='login'),
    path('refresh/',
         TokenRefreshView.as_view(),
         name='refresh'),
    path('activate/<str:token>/',
         ActivateUserView.as_view(),
         name='activate'),
    path('profile/',
         ProfileViewSet.as_view({'get': 'retrieve',
                                 'patch': 'update'}),
         name='profile',),
    path('password-change/',
         PasswordChangeView.as_view(),
         name='password_change',),
    path('password-change-done/',
         PasswordChangeDoneView.as_view(),
         name='password_change_done',),
    path('password-reset/', CustomPasswordResetView.as_view(),
         name='password_reset'),
    path('password-reset/done/',
         PasswordResetDoneView.as_view(),
         name='password_reset_done'),
    path('password-reset/confirm/<uidb64>/<token>/',
         CustomPasswordResetConfirmView.as_view(),
         name='password_reset_confirm'),
    path('password-reset/complete/',
         PasswordResetCompleteView.as_view(),
         name='password_reset_complete'),
    path('subjects/',
         SubjectsView.as_view(),
         name='subjects'),
    path('teacher/subjects/',
         UserSubjectViewSet.as_view({'get': 'list', 'patch': 'update',
                                     'post': 'create'}),
         name='teacher_subjects'),
    path('teacher/students/',
         TeacherStudentsViewSet.as_view({'get': 'list',
                                         'post': 'create'}),
         name='teacher_students',
         ),
    path('teacher/student/<int:pk>/',
         TeacherStudentsDetailViewSet.as_view({'get': 'retrieve',
                                               'delete': 'destroy',
                                               'patch': 'partial_update'}),
         name='teacher_student'),
    path('relate/student/<int:pk>/',
         RelateUnrelateStudentView.as_view(),
         name='relate'),
    path('confirm/<token>/',
         ConfirmView.as_view(),
         name='confirm'),
]
