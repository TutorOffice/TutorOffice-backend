from .models import Teacher


def get_user_type(request):
    try:
        profile = request.user.teacher_profile
        return 'teacher'
    except Teacher.DoesNotExist:
        return 'student'
