from clients.pagination import LessonAggregatePagination, LessonListPagination
from common.permissions import IsStudentOwner, IsTeacher, IsTeacherOwner
from clients.services import get_user_type
from django.utils.decorators import method_decorator
from django.views.decorators.cache import cache_page
from rest_framework.mixins import (
    CreateModelMixin,
    DestroyModelMixin,
    ListModelMixin,
    RetrieveModelMixin,
    UpdateModelMixin,
)
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.viewsets import GenericViewSet

from .filters import LessonFilter
from .models import Lesson
from .serializers import (
    StudentDetailLessonSerializer,
    StudentListLessonSerializer,
    TeacherDetailLessonSerializer,
    TeacherListLessonSerializer,
)


class AggregateLessonsViewSet(ListModelMixin, GenericViewSet):
    """
    Вьюсет для возврата количества уроков
    с возможностью выбора параметров для
    фильтрации и группировки данных.
    """

    filterset_class = LessonFilter
    pagination_class = LessonAggregatePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        """
        Возвращаются все уроки для учителя и ученика,
        в зависимости от типа профиля
        это осуществляется по-разному,
        т.к. ученик напрямую не связан с уроками
        """
        request = self.request
        profile = get_user_type(request)
        if profile == "teacher":
            return Lesson.objects.filter(teacher__user=request.user)
        return Lesson.objects.filter(
            teacher_student__student=request.user.student_profile
        )

    def list(self, request, *args, **kwargs):
        """
        Отфильтрованные данные группируются по выбранному параметру,
        по умолчанию это дата, но также имеется возможность по
        предметам, учителям для учеников и ученикам для учителей.
        """
        queryset = self.filter_queryset(self.get_queryset())
        group_by = request.query_params.get("group_by", None)
        match group_by:
            # добавить поле status в values
            case "subject":
                lessons = queryset.count_by_subjects()
            case "status":
                lessons = queryset.count_by_status()
            case "teacher":
                lessons = queryset.count_by_teachers()
            case "student":
                lessons = queryset.count_by_students()
            case _:
                lessons = queryset.count_by_date()
        return Response({"lessons": lessons})


class ListLessonViewSet(ListModelMixin, CreateModelMixin, GenericViewSet):
    """
    Возвращает список уроков с
    возможностью фильтрации.
    Позволяет создать урок учителю
    """

    filterset_class = LessonFilter
    pagination_class = LessonListPagination

    def get_permissions(self):
        if self.action == "create":
            return [IsAuthenticated(), IsTeacher()]
        return [IsAuthenticated()]

    def get_serializer_class(self):
        request = self.request
        profile = get_user_type(request)
        if profile == "teacher":
            return TeacherListLessonSerializer
        return StudentListLessonSerializer

    def get_queryset(self):
        request = self.request
        profile = get_user_type(request)
        if profile == "teacher":
            return Lesson.objects.select_related(
                "homework", "teacher_student"
            ).filter(teacher__user=request.user)
        return Lesson.objects.select_related(
            "teacher", "homework", "teacher__user"
        ).filter(teacher_student__student__user=request.user)

    def perform_create(self, serializer):
        """Метод создания учителя у урока."""
        user = self.request.user
        serializer.save(teacher=user.teacher_profile)


@method_decorator(cache_page(60 * 5), name="dispatch")
class DetailTeacherLessonViewSet(
    RetrieveModelMixin, UpdateModelMixin, DestroyModelMixin, GenericViewSet
):
    """
    Возвращает конкретный урок
    как для учителей, только учитель имеет право
    редактировать и удалять урок
    """

    http_method_names = ["get", "patch", "delete"]
    serializer_class = TeacherDetailLessonSerializer
    permission_classes = [IsAuthenticated, IsTeacherOwner]

    def get_queryset(self):
        return Lesson.objects.select_related(
            "homework", "subject", "teacher_student", "teacher__user"
        ).all()


@method_decorator(cache_page(60 * 5), name="dispatch")
class DetailStudentLessonViewSet(RetrieveModelMixin, GenericViewSet):
    """
    Возвращает конкретный урок для ученика,
    имеется только возможность чтения
    """

    serializer_class = StudentDetailLessonSerializer
    permission_classes = [IsAuthenticated, IsStudentOwner]
    queryset = Lesson.objects.all()

    def get_queryset(self):
        return Lesson.objects.select_related(
            "homework", "subject", "teacher"
        ).all()
