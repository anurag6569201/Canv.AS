from django import forms
from core.models import ProductReview,Address,profile,contactUs

class ProductReviewForm(forms.ModelForm):
    review=forms.CharField(widget=forms.Textarea(attrs={'placeholder':"Write review"}))

    class Meta:
        model=ProductReview
        fields=['review','rating']

class addressForm(forms.ModelForm):
    class Meta:
        model=Address
        fields=['address','mobile']

class profileForm(forms.ModelForm):
    class Meta:
        model = profile
        fields = ['image', 'full_name', 'bio', 'phone', 'email', 'website', 'github', 'twitter', 'instagram', 'facebook', 'verified']

class ContactForm(forms.Form):
    full_name = forms.CharField(max_length=200, required=True)
    phone = forms.CharField(max_length=200, required=True)
    email = forms.EmailField(required=True)
    subject = forms.CharField(max_length=200, required=True)
    message = forms.CharField(widget=forms.Textarea)