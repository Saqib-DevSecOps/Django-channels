from django.shortcuts import render

# Create your views here.

def index(request,channel_name):
    return render(request,'index.html',context={"channel_name":channel_name})