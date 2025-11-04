from rest_framework.generics import CreateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import SessionAuthentication
from .models import User
from .serializers import CreateUserSerializer
  

class CreateParentTeacherView(CreateAPIView):

    serializer_class = CreateUserSerializer
    queryset = User.objects.all()
    permission_classes = [IsAuthenticated]
    authentication_classes = [SessionAuthentication]

    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)
