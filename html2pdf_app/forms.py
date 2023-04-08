from django import forms
from .models import Bill, Rejected, Reexp, Appreciation, Termination, Offer, Intern

from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

class BillForm(forms.ModelForm):
    class Meta:
        model = Bill
        fields = "__all__"

class RejectedForm(forms.ModelForm):
    class Meta:
        model = Rejected 
        fields = "__all__"

class ReexpForm(forms.ModelForm):
    class Meta:
        model = Reexp 
        fields = "__all__"

class InternForm(forms.ModelForm):
    class Meta:
        model = Intern 
        fields = "__all__"

class AppreciationForm(forms.ModelForm):
    class Meta:
        model = Appreciation
        fields = "__all__"

class TerminationForm(forms.ModelForm):
    class Meta:
        model = Termination
        fields = "__all__"

class OfferForm(forms.ModelForm):
    class Meta:
        model = Offer
        fields = "__all__"

# Create your forms here.

class NewUserForm(UserCreationForm):
	email = forms.EmailField(required=True)

	class Meta:
		model = User
		fields = ("username", "email", "password1", "password2")

	def save(self, commit=True):
		user = super(NewUserForm, self).save(commit=False)
		user.email = self.cleaned_data['email']
		if commit:
			user.save()
		return user



class EmailForm(forms.Form):
    email = forms.EmailField()
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class LinkMail(forms.Form):

    message = forms.CharField()
    
    
    def __str__(self):
        return self.message

class RelivingEmailForm(forms.Form):
    email = forms.EmailField()
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class AppreciationEmailForm(forms.Form):
    email = forms.EmailField()
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class TerminationEmailForm(forms.Form):
    email = forms.EmailField()
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class OffernationEmailForm(forms.Form):
    email = forms.EmailField()
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))

class InternEmailForm(forms.Form):
    email = forms.EmailField()
    attach = forms.FileField(widget=forms.ClearableFileInput(attrs={'multiple': True}))