from django.contrib import admin

#Give admin access to the models in this app
from django.contrib import admin
from .models import School, UserRole, BaseForm, CustomForm, Application, AppAnswer, InterviewAvailability, InterviewSlot, Interview


admin.site.register(School)
admin.site.register(UserRole)
admin.site.register(BaseForm)
admin.site.register(CustomForm)
admin.site.register(Application)
admin.site.register(AppAnswer)
admin.site.register(InterviewAvailability)
admin.site.register(InterviewSlot)
admin.site.register(Interview)
