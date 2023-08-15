from rest_framework.pagination import PageNumberPagination


class SubjectsPagination(PageNumberPagination):
    """
    Класс пагинации для предметов
    """

    page_size = 10
    page_query_param = "page"


class UsersPagination(PageNumberPagination):
    """
    Класс пагинации для репетиторов ученика,
    а также учеников репетитора
    """

    page_size = 6
    page_query_param = "page"


class MaterialsPagination(PageNumberPagination):
    """
    Класс пагинации для материалов пользователей
    """

    page_size = 7
    page_query_param = "page"


class LessonListPagination(PageNumberPagination):
    """
    Класс пагинации для вывода
    списка уроков для пользователя
    """

    page_size = 5
    page_query_param = "page"


class LessonAggregatePagination(PageNumberPagination):
    """
    Класс пагинации для вывода
    агрегированных данных по урокам
    """

    page_size = 31
    page_query_param = "page"


class HomeworkListPagination(PageNumberPagination):
    """
    Класс пагинации для вывода
    списка ДЗ для пользователя
    """

    page_size = 5
    page_query_param = "page"


class HomeworkAggregatePagination(PageNumberPagination):
    """
    Класс пагинации для вывода
    агрегированных данных по ДЗ
    """

    page_size = 15
    page_query_param = "page"


class MessagePagination(PageNumberPagination):
    """
    Класс пагинации для вывода
    списка сообщений для пользователя
    """

    page_size = 20
    page_query_param = "page"
