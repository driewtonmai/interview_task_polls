from datetime import date

from django.http import Http404
from django.shortcuts import get_object_or_404, get_list_or_404
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Poll, UserSelectedPoll
from .serializers import ActivePollSerializer, ActivePollDetailSerializer, CreateAnswerSerializer, \
    UserSelectedPollSerializer, ListClientResultsSerializer, RetrieveClientResultsSerializer


class ActivePollListView(APIView):
    def get(self, request):
        queryset = Poll.objects.filter(start_date__lte=date.today(),
                                       end_date__gte=date.today(), draft=False)
        serializer = ActivePollSerializer(queryset, many=True, context={'request': request})
        return Response(serializer.data)


class ActivePollDetailView(APIView):
    def get_object(self, pk):
        try:
            return Poll.objects.filter(pk=pk, start_date__lte=date.today(),
                                       end_date__gte=date.today(), draft=False)
        except Poll.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        poll = self.get_object(pk)
        serializer = ActivePollDetailSerializer(poll, many=True)
        return Response(serializer.data)


class CreateAnswerView(APIView):
    def post(self, request):
        serializer = CreateAnswerSerializer(data=request.data, many=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class CreateUserSelectPollView(APIView):
    def post(self, request):
        serializer = UserSelectedPollSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ListClientResultsView(APIView):
    def get(self, request, pk):
        polls = get_list_or_404(UserSelectedPoll, client__id=pk)
        serializer = ListClientResultsSerializer(polls, many=True)
        return Response(serializer.data)


class RetrieveClientResultsView(APIView):
    def get(self, request, client_pk, selected_poll_pk):
        selected_poll = get_object_or_404(UserSelectedPoll, client__pk=client_pk, pk=selected_poll_pk)
        serializer = RetrieveClientResultsSerializer(selected_poll)
        return Response(serializer.data)