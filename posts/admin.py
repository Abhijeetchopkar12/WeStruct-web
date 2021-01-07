from django.contrib import admin

from .models import Author, Category, Post, Comment, PostView, Contact_us, Designation, Professionals, Student

admin.site.register(Author)
admin.site.register(Category)
admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(PostView)
admin.site.register(Contact_us)
admin.site.register(Professionals)
admin.site.register(Student)
admin.site.register(Designation)

