from django.contrib.auth.views import (
    PasswordChangeDoneView,
    PasswordChangeView,
    PasswordResetCompleteView,
    PasswordResetDoneView,
)
from django.urls import include, path
from rest_framework import routers
from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    ActivateUserView,
    ConfirmView,
    CustomPasswordResetConfirmView,
    CustomPasswordResetView,
    FeedbackViewSet,
    LoginView,
    ProfileViewSet,
    RegisterViewSet,
    RelateUnrelateStudentView,
    StudentTeachersViewSet,
    SubjectsView,
    TeacherStudentViewSet,
    UserSubjectViewSet,
)

# app_name = 'clients' тег url во встроенном reset-password шаблоне не работает

router = routers.DefaultRouter()
router.register("register", RegisterViewSet, basename="register")
router.register(
    "student/teachers", StudentTeachersViewSet, basename="student_teachers"
)
router.register(
    "teacher/students", TeacherStudentViewSet, basename="teacher_students"
)
router.register("feedback", FeedbackViewSet, basename="feedback")


urlpatterns = [
    path("", include(router.urls)),
    path("login/", LoginView.as_view(), name="login"),
    path("refresh/", TokenRefreshView.as_view(), name="refresh"),
    path("activate/<str:token>/", ActivateUserView.as_view(), name="activate"),
    path(
        "profile/",
        ProfileViewSet.as_view({"get": "retrieve", "patch": "update"}),
        name="profile",
    ),
    path(
        "password-change/",
        PasswordChangeView.as_view(),
        name="password_change",
    ),
    path(
        "password-change-done/",
        PasswordChangeDoneView.as_view(),
        name="password_change_done",
    ),
    path(
        "password-reset/",
        CustomPasswordResetView.as_view(),
        name="password_reset",
    ),
    path(
        "password-reset/done/",
        PasswordResetDoneView.as_view(),
        name="password_reset_done",
    ),
    path(
        "password-reset/confirm/<uidb64>/<token>/",
        CustomPasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(
        "password-reset/complete/",
        PasswordResetCompleteView.as_view(),
        name="password_reset_complete",
    ),
    path("subjects/", SubjectsView.as_view(), name="subjects"),
    path(
        "teacher/subjects/",
        UserSubjectViewSet.as_view(
            {"get": "list", "patch": "update", "post": "create"}
        ),
        name="teacher_subjects",
    ),
    path(
        "relate/student/<int:pk>/",
        RelateUnrelateStudentView.as_view(),
        name="relate",
    ),
    path("confirm/<token>/", ConfirmView.as_view(), name="confirm"),
]
