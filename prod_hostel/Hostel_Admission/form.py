from .models import Students_login 


from django import forms

class std_usr(forms.ModelForm):
  class Meta:
    model = Students_login
    fields = ['enrollment_no','passwd']
  
class category(forms.Form):
    id = forms.IntegerField()
    email = forms.CharField(max_length=255)

