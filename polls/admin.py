from django.contrib import admin

from .models import Poll, Question, QUESTION_TYPES, AnswerOptions, Answer, OptionChoices


admin.site.register(Poll)
admin.site.register(Question)
admin.site.register(AnswerOptions)
admin.site.register(Answer)
admin.site.register(OptionChoices)
