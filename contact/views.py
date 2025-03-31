from django.shortcuts import render, redirect
from .models import Contact,Category
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator

# Create your views here.
def contactHome(request):
    contacts = Contact.objects.all().filter(show=True).order_by('-id')
    
    paginator = Paginator(contacts, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'page_obj':page_obj,'site_title':'contatos - '}
    
    return render(request,'contact\index.html',context)

def contactDetails(request,contact_id):
    contact = Contact.objects.filter(id=contact_id,show=True).first()
    if(contact is None):
        raise Http404()
    contact_name = f'{contact.first_name} {contact.last_name} - ' 

    context = {'contact':contact,'site_title':contact_name}
    return render(request,'contact\contact.html',context)


def search(request):
    search_value = request.GET.get('q','').strip()
    if search_value == '':
        return redirect('contacts')
    contacts = Contact.objects.filter(show=True)\
        .filter(
            Q(first_name__icontains=search_value) | 
            Q(last_name__icontains=search_value) |
            Q(phone__icontains=search_value) |
            Q(email__icontains=search_value)
            )\
        .order_by('-id')
    paginator = Paginator(contacts, 25)
    page_number = request.GET.get("page")
    page_obj = paginator.get_page(page_number)
    context = {'page_obj':page_obj,'site_title':'contatos - '}
    return render(request,'contact\index.html',context)