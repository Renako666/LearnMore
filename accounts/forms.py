from django import forms
from django.contrib.auth.models import User
from .models import UserRole, UserProfile

class UserRoleForm(forms.Form):
    user = forms.ChoiceField(label='Select User')
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Only show users with student role
        student_users = User.objects.filter(role__role=UserRole.STUDENT)
        self.fields['user'].choices = [(user.id, user.username) for user in student_users]
        self.fields['user'].widget.attrs.update({'class': 'form-control'})

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ['bio']
        widgets = {
            'bio': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
        }
