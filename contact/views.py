from django.shortcuts import render

# Create your views here.
def contactHome(request):
    return render(request,'contact\index.html')
