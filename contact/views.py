from django.shortcuts import render
from .models import Contact,Category

# Create your views here.
def contactHome(request):
    contacts = Contact.objects.all()
    category = Category.objects.all()
    context = {'contacts':contacts,'categories':category}
    return render(request,'contact\index.html',context)
