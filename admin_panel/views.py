from django.http import Http404
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.authentication import BasicAuthentication
from rest_framework import status

from polls.models import Poll, Question, QuestionOptions, OptionChoices

from .serializers import AdminLoginSerializer, PollListSerializer, PollCreateSerializer, PollDetailSerializer


class AdminLoginView(APIView):
    authentication_classes = [BasicAuthentication]

    def post(self, request):
        serializer = AdminLoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        return Response({'msg': 'Добро пожаловать!', 'user': user.username})


class PollListCreateAPIView(APIView):
    permission_classes = [IsAdminUser]

    def get(self, request):
        queryset = Poll.objects.all()
        serializer = PollListSerializer(queryset, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PollCreateSerializer(data=request.data)
        user = request.user
        serializer.is_valid(raise_exception=True)
        serializer.save(created_by=user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class PollDetailView(APIView):
    permission_classes = [IsAdminUser]

    def get_object(self, pk):
        try:
            return Poll.objects.get(pk=pk)
        except Poll.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        poll = self.get_object(pk)
        serializer = PollDetailSerializer(poll)
        return Response(serializer.data)

    def put(self, request, pk):
        poll = self.get_object(pk)
        serializer = PollCreateSerializer(poll, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)

    def delete(self, request, pk):
        poll = self.get_object(pk)
        poll.delete()
        return Response(status.HTTP_204_NO_CONTENT)