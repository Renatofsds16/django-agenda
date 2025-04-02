from django import forms
from .models import Contact
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


6
class ContactForm(forms.ModelForm):


    picture = forms.ImageField(
        widget=forms.FileInput(
            attrs={
                'accept': 'image\*',
            }
        )
    )
    class Meta:
        model = Contact
        fields = 'first_name','last_name','phone','email','description','category','picture',


    def clean(self):
        clean_data = self.cleaned_data
        first_name = clean_data.get('first_name')
        last_name = clean_data.get('last_name')
        qtd = len(first_name)
        if first_name == last_name:
            self.add_error('first_name',ValidationError('name invalid',code=101))

        if  qtd < 2:
            self.add_error('first_name',ValidationError('nome muito curto'))
            self.add_error('last_name',ValidationError('nome muito curto'))
        
        return super().clean()
    



    def clean_first_name(self):
        first_name = self.cleaned_data.get('first_name')
        if first_name == 'abc':
            raise ValidationError('nao digite abc',code='invalid')
        return first_name


class RegisterForm(UserCreationForm):
    first_name = forms.CharField(
        required=True
    )
    last_name = forms.CharField(
        required=True
    )
    email = forms.EmailField(
        required=True
    )
    class Meta:
        model = User
        fields = 'first_name','last_name','email','username','password1','password2',


    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            self.add_error('email',ValidationError('email ja existe'))
        return email
        
