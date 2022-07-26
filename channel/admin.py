from django.contrib import admin

# Register your models here.
from channel.models import Chat, Group

admin.site.register(Group)
admin.site.register(Chat)