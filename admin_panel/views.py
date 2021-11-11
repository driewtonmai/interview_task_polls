from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication

from .serializers import AdminLoginSerializer


class AdminLoginView(APIView):
    authentication_classes = [BasicAuthentication]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({'msg': 'Добро пожаловать!', 'user': user.username})
