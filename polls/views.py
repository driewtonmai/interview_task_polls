from datetime import date

from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response

from .models import Question, Answer, AnswerOptions, OptionChoices, Poll
from .serializers import ActivePollSerializer


class ListActivePollsView(APIView):
    def get(self, request):
        queryset = Poll.objects.filter(start_date__lte=date.today(),
                                       end_date__gte=date.today(), draft=False)
        serializer = ActivePollSerializer(queryset, many=True)
        return Response(serializer.data)
