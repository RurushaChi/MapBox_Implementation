from django.contrib import admin

#Give admin access to the models in this app
from django.contrib import admin
from .models import School, Staff, BaseForm, CustomForm, Application, AppAnswer


admin.site.register(School)
admin.site.register(Staff)
admin.site.register(BaseForm)
admin.site.register(CustomForm)
admin.site.register(Application)
admin.site.register(AppAnswer)