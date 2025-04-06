from django.shortcuts import render, redirect, get_object_or_404
from .models import Contact
from django.http import Http404
from django.db.models import Q
from django.core.paginator import Paginator
from .forms import ContactForm, RegisterForm, RegisterUpdateForm
from django.urls import reverse
from django.contrib.auth.forms import AuthenticationForm
from django.contrib import messages
from django.contrib import auth
from django.contrib.auth.decorators import login_required




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

@login_required(login_url='login')
def create(request):
    form_action = reverse('create')
    if request.method == 'POST':
        form = ContactForm(request.POST,request.FILES)
        context = {'form':form,'form_action':form_action}
        if form.is_valid():
            contact: Contact = form.save(commit=False)
            contact.owner = request.user
            contact.save()
            return redirect('contacts')
        return render(request,'contact\create.html',context)
    
    context = {'form':ContactForm(),'form_action':form_action}
    return render(request,'contact\create.html',context)
    
@login_required(login_url='login')
def update(request,contact_id):
    contact = get_object_or_404(Contact,id=contact_id,show=True,owner=request.user)
    form_action = reverse('update',args=(contact_id,))
    
    if request.method == 'POST':
  
        form = ContactForm(request.POST,request.FILES,instance=contact)
        context = {'form':form,'form_action':form_action}
        if form.is_valid():
            form.save()
            return redirect('contacts')
        return render(request,'contact\create.html',context)
    
    context = {'form':ContactForm(instance=contact),'form_action':form_action}
    return render(request,'contact\create.html',context)

@login_required(login_url='login')
def delete(request,contact_id):
    contact = get_object_or_404(Contact,id=contact_id,show=True,owner=request.user)
    confirmation = request.POST.get('confirmation','no')
    if confirmation == 'yes':
        contact.delete()
        return redirect('contacts')

    return render(request,'contact\contact.html',{'contact':contact,'confirmation':confirmation})


def register(request):
    form = RegisterForm()
    #messages.info(request,'ola mundo')
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            form.save()
            redirect('contacts')
    return render(request,'contact/register.html',{'form':form})

def login_view(request):
    form = AuthenticationForm(request)
    if request.method == 'POST':
        form = AuthenticationForm(request,request.POST)
        if form.is_valid():
            user = form.get_user()
            print(user)
            auth.login(request,user)
            messages.success(request,'logado com sucesso!')
            return redirect('contacts')
        else:
            messages.error(request,'não foi posivel fazer login')
    return render(request,'contact/login.html',{'form':form})
@login_required(login_url='login')
def logout_view(request):
    auth.logout(request)
    return redirect('login')
@login_required(login_url='login')
def user_update(request):
    form = RegisterUpdateForm(instance=request.user)
    if request.method == 'POST':
        form = RegisterUpdateForm(instance=request.user,data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('contacts')
    return render(request,'contact/register.html',{'form':form})
    