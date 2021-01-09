import django_filters
from .models import Author, User


class AuthorFilter(django_filters.FilterSet):
    class Meta:
        model = Author
        fields = '__all__'
        exclude = ['profile_picture', 'user', 'profile_picture', 'bio', 'phone_number', 'address', 'date_of_birth', 'rating', 'date_created','cover_picture' ]

class UserFilter(django_filters.FilterSet):
    class Meta:
        model = User
        fields = '__all__'
        placeholder = "UserName"
        exclude = ['password','last_login', 'is_superuser','groups','user_permissions','first_name','last_name','email','is_staff', 'is_active','date_joined','following']

