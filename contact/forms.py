from django import forms
from .models import Contact
from django.core.exceptions import ValidationError
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation


6
class ContactForm(forms.ModelForm):


    picture = forms.ImageField(
        required=False,
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


class RegisterUpdateForm(forms.ModelForm):
    first_name = forms.CharField(
        min_length=2,
        max_length=50,
        required=True,
        error_messages= {
            'min_length': 'por favor digite 2 letras ou mais'
        }
    )
    last_name = forms.CharField(
        min_length=2,
        max_length=50,
        required=True,
        error_messages= {
            'min_length': 'por favor digite 2 letras ou mais'
        }
    )

    password1 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}),
        help_text=password_validation.password_validators_help_text_html(),
        required=False
    )

    password2 = forms.CharField(
        label='Password',
        strip=False,
        widget=forms.PasswordInput(attrs={'autocomplete':'new-password'}),
        help_text='as senha deven ser iguais',
        required=False,
    )
    class Meta:
        model = User
        fields = 'first_name','last_name','email','username',

    def clean_email(self):
        email = self.cleaned_data.get('email')
        current_email = self.instance.email
        if current_email != email:
            if User.objects.filter(email=email).exists():
                self.add_error('email',ValidationError('email ja existe'))
        return email
    
    def clean_password1(self):
        password1 = self.cleaned_data.get('password1')
        if password1:
            try:
                password_validation.validate_password(password1)
            except ValidationError as error:
                self.add_error('password1',ValidationError(error))
        return password1
    
    def clean(self):
        password1 = self.cleaned_data.get('password1')
        password2 = self.cleaned_data.get('password2')
        if password1 or password2:
            if password1 != password2:
                self.add_error('password2',ValidationError('as senha nao são iguais'))

        return super().clean()
    
    def save(self, commit=True):
        cleaned_data = self.cleaned_data
        user: User = super().save(commit=False)
        password = cleaned_data.get('password1')
        if password:
            user.set_password(password)

        if commit:
            user.save()

        

        return user

        

