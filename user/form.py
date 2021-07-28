from django.contrib.auth.forms import UserCreationForm
from .models import MyUser
from django import forms

# define MyUser form for user register
class MyUserCreationForm(UserCreationForm):
    # init function
    def __init__(self, *args, **kwargs):
        super(MyUserCreationForm, self).__init__(*args, **kwargs)
        self.fields['password1'].widget = forms.PasswordInput(attrs={'class': 'txt tabInput', 'placeholder':'book store password require'})
        self.fields['password2'].widget = forms.PasswordInput(attrs={'class': 'txt tabInput', 'placeholder':'repeat password'})
    class Meta(UserCreationForm.Meta):
        model = MyUser
        #add mobile
        fields = UserCreationForm.Meta.fields +('mobile',)
        # set style and attribute
        widgets = {
            'mobile': forms.widgets.TextInput(attrs={'class': 'txt tabInput', 'placeholder':'phone number'}),
            'username': forms.widgets.TextInput(attrs={'class': 'txt tabInput', 'placeholder':'unique username'}),
        }
