from django.contrib import admin
from .models import User, Egg,ChicksManagement, FeedingTimeTable
# Register your models here.

admin.site.register(User)
admin.site.register(Egg)
admin.site.register(FeedingTimeTable)
admin.site.register(ChicksManagement)