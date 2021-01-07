from django import forms
from tinymce import TinyMCE
from django.contrib.auth.models import User
from .models import Post, Comment, Author, Contact_us

class TinyMCEWidget(TinyMCE):
    def use_required_attribute(self, *args):
        return False


class PostForm(forms.ModelForm):
    
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

    tags = forms.CharField(widget=forms.TextInput(attrs={'data-role': 'tagsinput'}), required=False)
         
    class Meta:
        model = Post
        fields = ('title', 'overview', 'content', 'thumbnail', 
        'categories', 'tags', 'featured', 'previous_post', 'next_post')


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


class ContactForm(forms.ModelForm):
    name = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Name', 'class': 'form-control'}))
    phone_number = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Phone Number', 'class': 'form-control'}))
    email = forms.EmailField(widget=forms.TextInput(attrs={'placeholder': 'Your E-mail', 'class': 'form-control'}))
    subject = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Your Subject', 'class': 'form-control'}))
    message = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Your Message', 'class': 'form-control'}))

    class Meta:
        model = Contact_us
        fields = ['name', 'phone_number', 'email', 'subject', 'massage']


class UserUpdate(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']
        # name.widget.attrs.({'class': 'form-control'})


class DateInput(forms.DateInput):
    input_type = 'date'


class ProfileUpdate(forms.ModelForm):
    date_of_birth = forms.DateField(widget=DateInput())
    
    address = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'Address', 'class': ' city '}))
    city = forms.CharField(widget=forms.TextInput(attrs={'placeholder': 'city', 'class': 'city '}))


    professionals_check = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input check che', 'id': 'exampleCheck1 id_professionals_check', 'onclick': 'professionals_check()'}
            ), required=False
        )

    student_check = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input check che', 'id': 'exampleCheck2 id_student_check', 'onclick': 'student_check()'}
            ), required=False
        )

    user_check = forms.BooleanField(
        widget=forms.CheckboxInput(
            attrs={'class': 'form-check-input check che', 'id': 'exampleCheck3 id_user_check', 'onclick': 'user_check()'}
            ), required=False
        )

    class Meta:
        model = Author
        fields =['bio', 'phone_number', 'date_of_birth', 'profile_picture', 'cover_picture', 'professionals_check', 'student_check', 'user_check', 'professionals', 'student', 'address', 'city', 'postal_code', 'verified_tick']
        # designation 
