from django import forms
from .models import UserProfile

class UserProfileForm(forms.ModelForm):
    def clean_phone(self):
        phone = self.cleaned_data.get('phone')
        import re
        if phone and not re.match(r'^\+?\d{7,15}$', phone):
            raise forms.ValidationError('Enter a valid phone number.')
        return phone
    class Meta:
        model = UserProfile
        fields = ['phone', 'address', 'avatar']
        widgets = {
            'phone': forms.TextInput(attrs={'class': 'input input-bordered w-full'}),
            'address': forms.Textarea(attrs={'class': 'textarea textarea-bordered w-full', 'rows': 3}),
            'avatar': forms.FileInput(attrs={'class': 'file-input file-input-bordered w-full'}),
        }

# Placeholder for future ReviewForm
# class ReviewForm(forms.ModelForm):
#     class Meta:
#         model = Review
#         fields = ['rating', 'comment'] 