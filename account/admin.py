from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Profile,Company,Languages,About_me,ActorCategory,ModelCategory,ProductionCategory,Popular

admin.site.register(Profile)
admin.site.register(Company)
admin.site.register(Languages)
admin.site.register(ActorCategory)
admin.site.register(ModelCategory)
admin.site.register(ProductionCategory)
admin.site.register(About_me)
admin.site.register(Popular)




