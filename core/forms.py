from django import forms
from core.models import ProductReview,Address,profile

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