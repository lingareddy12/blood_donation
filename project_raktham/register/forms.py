from django import forms
from .models import user_registration,acceptor

class regist_form(forms.ModelForm):
    class Meta:
        model = user_registration
        fields = ['username','email','password']

    def __init__(self, *args, **kwargs):
        super(regist_form, self).__init__(*args, **kwargs)
        self.fields['password'].widget = forms.PasswordInput()   
        

        
        
