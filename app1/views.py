
from django.shortcuts import render, HttpResponse, redirect
from . import models
from django.contrib import messages

def index(request):
    models.test_many_to_many(1,1)
    return render(request, "index.html" )


def login(request):
    # mylist = [  "Apple" , "strawberry" , "Lemon" ,"Blackberry"  , "Mango"  ]

    # for i in range ( 0, len(mylist), 1):
    #     if mylist[i] is "Mango":
    #         mylist.pop(i)

    context = {
        #key           #value
        "firstname" : "Mohammad",
        "lastname" : "Khaseeb",
    }
    return render(request , "login.html", context)   #render_template
    # return render_template("inde.html" , firstname="", lastname="")

def display_matches(request,leagueId,leagueCountry):
    if request.method == "GET": #GET,POST, PUT, PATCH, DELETE
        print(leagueCountry)
        print(leagueId)
        return render( request , "login.html" )
    else:
        return redirect('/')
    
#Get reg html page
def reg_form(request):
    return render(request , "reg.html")

#Post submission
def reg_form_post(request):
    if request.method == "POST":

        errors = models.User.objects.reg_validator(request.POST)
        if len(errors) > 0:
            for key, value in errors.items():
                messages.error(request, value)
            return redirect('/reg')
        else:
            name = request.POST['name']
            phonenumber = request.POST['phonenumber']
            #address = request.POST['address']

            print(name)
            print(phonenumber)
            #print(address)
            
            myuser = models.create_user( request.POST)

            request.session['name'] = name
            request.session["is_logged"] = True
            request.session["id"] = myuser.id
        
            return redirect("/home")
    else:
        return redirect("/")
    


def home_page(request):
    if 'is_logged' in request.session:
        omar = {
            'users' : models.get_all_users()
        }
        return render(request , "home.html", omar)
    else:
        return redirect("/login")

def logout(request):
    del request.session['name']
    del request.session['is_logged']
    del request.session['id']
    #request.session.clear()
    return redirect("/")


def update_user(request):
    context = {
        'user' : models.get_user(request.session['id'])
    }
    return render(request , "updateuser.html" , context)


#ORM and post requset will be done here!
def update_post(request):
    if request.method == "POST":
        name = request.POST['new_name']
        phonenumber = request.POST['new_phonenumber']
        #address = request.POST['new_address']
        id = request.POST['user_id']

        updateduser = models.get_user( id)
        updateduser.name = name
        updateduser.phonenumber = phonenumber
        #updateduser.address = address

        updateduser.save()
        return redirect("/home")
    else:
        return redirect("/")
    

def delete_form(request):
    if request.method == "POST":
        if 'id' in request.session:
            models.delete_user_from_DB( request.session['id'])
            return redirect("/logout")
        else:
            return redirect("/")
    else:
        return redirect("/")
    
def delete_by_user_id(request):
    if request.method == "POST":
        models.delete_user_from_DB( request.POST['user_id'])
        return redirect("/home")
    else:
        return redirect("/")
    

def addaddress(request):
    return render(request , "addaddress.html")

def address_add_form(request):
    city = request.POST['city']
    country = request.POST['country']
    street = request.POST['street']
    id= request.session['id']
    mohammadKhaseeb = models.User.objects.get(id = id)
    myaddress = models.Address.objects.create( city = city , country = country, street = street , user =  mohammadKhaseeb)

    return redirect("/home")


def show_addresses(request):
    id = request.session['id']
    context = {
        'myuser' : models.get_all_address(id)

    }
    return render(request , 'showaddresses.html',context)

#This method will handle the login form POST request from landing page
def login_form(request):
    if request.method == "POST":
        name = request.POST['name']
        password = request.POST['password']
        result = models.login_check(request)
        if (result):
            return redirect("/home")
        else:
            context = {
            'msg' : "Username or password does not exist!"
        }
        return render(request, "index.html", context)
    else:  # post request 
        context = {
            'msg' : "Bad request"
        }
        return render(request, "index.html", context) 
    