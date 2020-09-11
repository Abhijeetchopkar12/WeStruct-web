from django import forms
from tinymce import TinyMCE
from django.contrib.auth.models import User
from .models import Post, Comment, Author


class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    # user = forms.CharField(
    #     widget=forms.ModelChoiceField(
    #         attrs={'required': True, 'cols': 30, 'rows': 1}
    #         )
    # )
    content = forms.CharField(
        widget=TinyMCEWidget(
            attrs={'required': False, 'cols': 30, 'rows': 10}
        )
    )
    overview = forms.CharField(
        widget=forms.Textarea(
            attrs={'required': True, 'cols': 40, 'rows': 5}
        )
    )
    
    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail', 
        'categories', 'featured', 'previous_post', 'next_post')


class CommentForm(forms.ModelForm):
    content = forms.CharField(widget=forms.Textarea(attrs={
        'class': 'form-control',
        'placeholder': 'Type your comment',
        'id': 'usercomment',
        'rows': '4'
    }))
    class Meta:
        model = Comment
        fields = ('content', )


class ContactForm(forms.Form):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your E-mail', 'class': 'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Subject', 'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message', 'class': 'form-control'}))

class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # name.widget.attrs.({'class': 'form-control'})

class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileUpdate(forms.ModelForm):
    date_of_birth = forms.DateField(widget=DateInput())

    class Meta:
        model = Author
        fields =['bio', 'phone_number', 'date_of_birth', 'profile_picture']
        # name.widget.attrs.({'class': 'form-control'})