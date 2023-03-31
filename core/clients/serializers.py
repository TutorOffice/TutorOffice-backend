from rest_framework import serializers
from .models import User, Teacher, Student, Subject, TeacherStudent
from django.db.transaction import atomic
from django.contrib.auth.hashers import make_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError


# Сериализатор для обработки формы регистрации
class RegisterSerializer(serializers.ModelSerializer):
    is_teacher = serializers.BooleanField(
        required=True,
        write_only=True,
    )
    password = serializers.CharField(
        required=True,
        write_only=True,
        validators=[
            validate_password,
        ]
    )
    password2 = serializers.CharField(
        required=True,
        write_only=True,
    )

    # Поля взяты из .models.User
    class Meta:
        model = User
        fields = [
            'id',
            'first_name',
            'patronymic_name',
            'last_name',
            'email',
            'phone',
            'is_teacher',
            'password',
            'password2',
        ]

    # Проверка совпадающих паролей в форме регистрации
    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise ValidationError({
                'password': 'Пароли не совпадают',
                'password2': 'Пароли не совпадают',
            })
        attrs.pop('password2')
        return attrs

    # Переопределение метода create.
    # В случае ошибочного ввода данных НЕ сохраняет строки в БД
    @atomic
    def create(self, validated_data):
        role = validated_data.pop('is_teacher', None)
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.password = make_password(password)
        user.save()
        if role:
            Teacher.objects.create(user=user)
        else:
            Student.objects.create(user=user)
        return user


class ProfileSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = (
            'id',
            'first_name',
            'patronymic_name',
            'last_name',
            'phone',
            'email',
            'photo',
        )
        read_only_fields = ('id', 'email', 'photo')


class SubjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обработки
    получения всех предметов
    """
    class Meta:
        model = Subject
        fields = '__all__'


class UserSubjectSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обработки получения,
    добавления и обновления предметов репетитора
    """
    subjects = serializers.PrimaryKeyRelatedField(
        queryset=Subject.objects.all(),
        many=True)
    titles = serializers.StringRelatedField(
        source='subjects',
        read_only=True,
        many=True
    )

    class Meta:
        model = Teacher
        fields = ('subjects', 'titles')

    def create(self, validated_data):
        subjects = validated_data.pop('subjects')
        user = self.context['request'].user
        teacher = Teacher.objects.get(user=user)
        if teacher.subjects.exists():
            raise serializers.ValidationError({
                "subjects": "Эта функция больше недоступна! "
                "Вы можете обновить перечень ваших предметов!"})
        teacher.subjects.set(subjects)
        teacher.save()
        return teacher

    def update(self, instance, validated_data):
        subjects = validated_data['subjects']
        instance.subjects.set(subjects)
        instance.save()
        return instance


class TeacherStudentSerializer(serializers.ModelSerializer):
    """
    Сериализатор для обработки CRUD-операций, связанных
    с учениками репетитора
    """
    class Meta:
        model = TeacherStudent
        fields = (
            'id',
            'last_name',
            'first_name',
            'patronymic_name',
            'phone',
            'email',
            'comment',
        )
        read_only_fields = ('id',)

    def validate(self, attrs):
        if self.context['request'].method == 'PATCH':
            email = attrs['email'] or None
            if email:
                raise serializers.ValidationError(
                    {"email": "Вы не можете обновлять почту добавленных пользователей! "
                              "Вам нужно добавить нового пользователя!"})
        else:
            email = attrs['email']
            teacher = self.context['request'].user.teacher_profile
            if email == self.context['request'].user.email:
                raise serializers.ValidationError({"email": "Вы не можете добавить себя в качестве ученика!"})
            if TeacherStudent.objects.filter(teacher=teacher, email=email).exists():
                raise serializers.ValidationError({"email": "У вас уже есть ученик с такой почтой!"})
        return attrs
