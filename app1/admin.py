from django.contrib import admin
from .models import  * # replace with your model

admin.site.register(User)
admin.site.register(Book)
admin.site.register(Publisher)
admin.site.register(Address)


