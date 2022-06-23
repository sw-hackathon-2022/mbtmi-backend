from django.contrib import admin

from surveys.models import Survey, SurveyReply, SurveyItem

admin.site.register(Survey)
admin.site.register(SurveyItem)
admin.site.register(SurveyReply)
