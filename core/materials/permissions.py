from common.permissions import IsStudent


class IsStudentMaterialOwner(IsStudent):
    """
    Ограничение проверяет, относится ли
    этот ученик к материалу
    """

    def has_object_permission(self, request, view, obj):
        queryset = obj.teacher_student.all()
        students = [entry.student for entry in queryset]
        if request.user.student_profile in students:
            return True
        return False
