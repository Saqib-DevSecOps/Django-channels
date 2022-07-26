import json

from django.shortcuts import render

# Create your views here.
from channel.models import Group, Chat


def index(request,channel_name):
    channel_name ,created= Group.objects.get_or_create(name=channel_name)
    chat = Chat.objects.filter(group = channel_name)
    return render(request,'index.html',context={"channel_name":channel_name.name,
                                                "chat":chat})