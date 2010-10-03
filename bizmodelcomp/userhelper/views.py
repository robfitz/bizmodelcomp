from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User



def noPermissions(request):

    return render_to_response('/userhelper/no_permissions.html')


def loginUser(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')
    
    alert = None

    if request.method == "POST" and len(request.POST) > 0:
        email = request.POST["email"]
        password = request.POST["password"]
        user = auth.authenticate(username=email, password=password)
        if user is not None:
            #logged in successfully
            login(request, user)

            try: next = request.POST["next"]
            except: next = "/dashboard/"
            
            return HttpResponseRedirect(next)
        
        else:
            #login failed
            alert = "Login failed. Try again?"

    elif request.method == "GET":
        #page to redirect to after success
        next = request.GET.get("next", "/dashboard")

            
    return render_to_response('userhelper/login.html', locals())



def logoutUser(request):
    auth.logout(request)
    return HttpResponseRedirect('/') #back to the index



def registerUser(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')
    
    alert = None

    default_code = ""
    try:
        default_code = request.GET["code"]
    except:
        pass

    if request.method == "POST":

        email = request.POST["email"]
        pass1 = request.POST["password1"]
        pass2 = request.POST["password2"]
        
        discount_code = default_code
        if request.POST["discount_code"]:
            discount_code = request.POST["discount_code"]
            print 'discount %s' % discount_code

        #TODO: non-hardcoded trial account_type
        user = createNewUser(request, email, pass1, pass2, "default", discount_code)

        if user is not None:

            try: next = request.POST["next"]
            except: next = "/dashboard/"
            
            return HttpResponseRedirect(next)
        
        else:
            alert = "Passwords don't match or your email isn't valid. Try again?"

    elif request.method == "GET":
        #page to redirect to after success
        next = request.GET.get("next", "/dashboard")

    return render_to_response('userhelper/register.html', locals())



def createNewUser(request, email, pass1, pass2, account_type, discount_code=None):

    if email is not None and pass1 == pass2:
            user = User.objects.create_user(username=email,
                                            email=email,
                                            password = pass1)
            if user is not None:
                user.save()
                user = auth.authenticate(username=email, password=pass1)            
                if user is not None:
##                    user_info = UserInfo(user=user,
##                                         account_type=account_type)
##                    user_info.save()
                    #successful login
                    login(request, user)

                    #check for valid discount code
##                    if discount_code is not None:
##                        try:
##                            code = DiscountCodeTemplate.objects.filter(code=discount_code)[0]
##                            user_discount = code.newDiscountCode(user)
##                            if not user_discount:
##                                #TODO: alert user that their code failed and prompt them
##                                #to re-enter it
##                                pass
##                        except:
##                            pass

                    return user

                else:
                    print "We couldn't log in to your new account. Try again?"
                    return None
            else:
                print "We couldn't create your account successfully. Try again?"
                return None
    else:
        print "Create new user big 'else'"
        return None
    
