from django.contrib import admin

from .models import Poll, Question, Answer, OptionChoices, UserSelectedPoll, AnswerOptions


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(OptionChoices)
admin.site.register(UserSelectedPoll)
admin.site.register(AnswerOptions)
