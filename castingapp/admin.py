from django.contrib import admin

# Register your models here.
from castingapp.models import *

admin.site.register(News)
admin.site.register(Favourites)
admin.site.register(CardItem)
admin.site.register(SentCard)
admin.site.register(Partners)