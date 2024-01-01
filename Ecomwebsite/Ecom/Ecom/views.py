from django.shortcuts import HttpResponse
from django.shortcuts import render,redirect

def main(request):
    return render(request,'index.html')
