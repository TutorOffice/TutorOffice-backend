from rest_framework.viewsets import ModelViewSet
from rest_framework.filters import SearchFilter
from .models import Homework, Lesson
from .serializers import HomeworkSerializer, LessonSerializer
from clients.models import Teacher, Student, User
from django.shortcuts import get_object_or_404


class HomeworkViewSet(ModelViewSet):
    """ViewSet для эндпойнта /homeworks/
    c пагинацией и поиском по полю title"""

    serializer_class = HomeworkSerializer
    queryset = Homework.objects.all()
#    filter_backends = (SearchFilter,)
#    search_fields = ('title',)
#    #pagination_class = LimitOffsetPagination
#    #permission_classes = (
#    #    IsAuthenticatedOrReadOnly,
#    #    IsAdminOnly,
#   #)


class LessonViewSet(ModelViewSet):
    """ViewSet для эндпойнта /lessons/
    c пагинацией и поиском ..."""

    serializer_class = LessonSerializer
    queryset = Lesson.objects.all()
#    permission_classes = (
#        IsAuthenticatedOrReadOnly,
#        IsAuthorOrIsStaffPermission,
#    )

#    def get_queryset(self):
#        """Метод обработки запроса."""
#        teacher_id = self.request.user
#        teacher = get_object_or_404(Teacher, id=teacher_id)
#        return teacher.lessons.all()

    def perform_create(self, serializer):
        """Метод пeреопределения автора."""
        serializer.save(teacher=self.request.user)

 #   def get_serializer_class(self):
#        """Метод предопределения сериализатора в зависимости от запроса."""
 #       if self.action in ("list", "retrieve"):
 #           return LessonSerializer
 #       return LessonCreateSerializer