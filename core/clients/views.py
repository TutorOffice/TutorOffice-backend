from clients.models import User
from clients.serializers import RegisterSerializer
from rest_framework.generics import CreateAPIView
from rest_framework.viewsets import GenericViewSet
# Create your views here.


class RegisterView(CreateAPIView, GenericViewSet):
    queryset = User.objects.all()
    serializer_class = RegisterSerializer
