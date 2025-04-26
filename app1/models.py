from django.db import models
from datetime import datetime
import re
import bcrypt

class UserManager(models.Manager):
    def reg_validator(self , post):
        errors = {} 
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if len(post['name']) == 0:
            errors['user_name'] ="Name is required!"
        if len(post['name']) < 9:
            errors['name_length'] ="Name must be more than 9"
        if len(post['phonenumber']) == 0:
            errors['phonenumber'] ="Phonenumber is required!"
        if len(post['phonenumber']) != 10:
            errors['phonenumber_length'] ="Phone number must be 10 digits"  
        return errors
    
    # def login_validator(self, loginform):

# class AddressManager(models.manager):
#     def address_val(self,)
    
# Create your models here.
class User(models.Model): 
    # id
    name = models.CharField(max_length=30) # equivilent to varchar(30)
    #first_name =  models.CharField(max_length=30) 
    #last_name =  models.CharField(max_length=30)
    password = models.CharField(max_length=255,default="password123")
    phonenumber = models.CharField(max_length=14)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #addresses
    objects = UserManager()



class Address(models.Model):
    #id
    country = models.CharField(max_length=30)
    city = models.CharField(max_length=30)
    street = models.CharField(max_length=100)
    user = models.ForeignKey( User, related_name="addresses" ,on_delete=models.DO_NOTHING )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class Publisher(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    #books

class Book(models.Model):
    title = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    publishers = models.ManyToManyField(Publisher,related_name='books')



#This function will return all users from users table in DB
def get_all_users():
    return User.objects.all()

#This function will return user by id from users table in DB
def get_user(id):
    return User.objects.get(id = id)

def create_user(post):
    pw_hash = bcrypt.hashpw(post['password'].encode(), bcrypt.gensalt()).decode()
    return User.objects.create( name = post['name'] , phonenumber = post['phonenumber'], password = pw_hash)


                        #None
def delete_user_from_DB(id):
    my_user = User.objects.get( id = id)
    my_user.delete()

def get_all_address(user_id):
    return User.objects.get(id = user_id)
    

                        #  1     1
def test_many_to_many(book_id , publisher_id):
    mybook = Book.objects.get(id = book_id)  #Gone with wind
    mypublisher = Publisher.objects.get(id = publisher_id) #Majd H.

    mybook.publishers.remove(mypublisher)

    #mypublisher.books.add(mybook)

def login_check(postdata):
    name = postdata.POST['name']
    password = postdata.POST['password']
    user = User.objects.get(name = name)
    if bcrypt.checkpw(password.encode(), user.password.encode()):
        print("password match")
        postdata.session['name'] = name
        postdata.session["is_logged"] = True
        postdata.session["id"] = user.id
        return True
    else:
        print("failed password")
        return False



