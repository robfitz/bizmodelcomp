from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.models import User

from settings import ACCOUNT_EMAIL_CONFIRM_REQUIRED
from userhelper.util import *
from userhelper.models import *
from judge.models import *
from utils.util import rand_key

from competition.models import *

def noPermissions(request):

    return render_to_response('userhelper/no_permissions.html')



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
            except:
                
                if len(Competition.objects.filter(owner=user)) > 0:
                    next = "/dashboard/"
                else:
                    next = "/judge/"
            
            return HttpResponseRedirect(next)
        
        else:
            #login failed
            alert = "Login failed. Try again?"

    elif request.method == "GET":
        #page to redirect to after success
        next = request.GET.get("next", "/dashboard")

        email = request.GET.get("e", "")

    

            
    return render_to_response('userhelper/login.html', locals())



def logoutUser(request):
    auth.logout(request)
    return HttpResponseRedirect('/') #back to the index



def is_new_user_judge(user):
    print 'is new user judge? user=%s, email=%s' % (user, user.email)
    try:
        #is new acct meant to be a judgeman?
        judge = JudgeInvitation.objects.get(email=user.email)
        print 'judge = %s' % judge
        judge.user = user
        judge.save()
        print 'saved judge, returning true'
        return judge
    except:
        #not a judge
        return False



def registerUser(request):

    if request.user.is_authenticated():
       return HttpResponseRedirect('/dashboard/')
    
    alert = None

    if request.method == "POST":

        email = request.POST["email"]
        pass1 = request.POST["password1"]
        pass2 = request.POST["password2"]
            
        user = None
        try:
                user = createNewUser(request, email, pass1, pass2)
        except:
            next = request.POST.get("next")
            login = "/accounts/login/"
            if next:
                login += "?next=%s" % next
            alert = "That email has already been registered. Try <a href='%s'>logging in</a> instead?" % login

        try:
            #is there a verification key already hooked up to that email?
            key = VerificationKey.objects.get(email=user.email)
            key.user = user
            key.save()
        except: pass

        if user is not None:

            is_judge = is_new_user_judge(user)
            print 'so was it a judge? %s' % is_judge

            if is_judge:
                next = "/judge/"
            else: 
                next = request.POST.get("next")
                if not next:
                    #if we don't have an explicitly set next page, we take our best guess
                    next = "/dashboard/"

            print 'go here next: %s' % next

            #require email confirmation?
            if ACCOUNT_EMAIL_CONFIRM_REQUIRED:
                user.is_active = False
                user.save()

                #send a verification link for them to clicky click
                try:
                    key = VerificationKey.objects.get(user=user)

                    if key.is_verified:
                        #this email has already been verified somehow,
                        #like clicking on an email-only link. so we don't
                        #need to check it again. yays.
                        user.is_active = True
                        user.save()
                        return HttpResponseRedirect(next)
                    
                    else:
                        send_verification_email(user, next)
                except:
                    send_verification_email(user, next)

                #display a page telling them what's going on
                return HttpResponseRedirect("/accounts/verify_email/?next=%s" % next)
            
            #successfully made a user and don't require email confirmation, 
            #so redirect to next page
            return HttpResponseRedirect(next)
                                            
        elif not alert:
            #if we failed to make a user and don't have a more specific alert, 
            #go with a generic fail message
            alert = "Passwords don't match or your email isn't valid. Try again?"


    elif request.method == "GET":
                                
        #page to redirect to after success
        next = request.GET.get("next", "/dashboard/")

        email = request.GET.get("e", "")

        #if they got to the judging page from the email link,
        #we can verify their email right now
        got_ev_key(request.GET.get("ev", False))
            
    return render_to_response('userhelper/register.html', locals())



#display a page telling them they need to go click that email
def verify_email(request):

    return render_to_response('userhelper/verify_email.html')



def createNewUser(request, email, pass1, pass2, account_type="default", discount_code=None):

    if email is not None and pass1 == pass2:
            user = User.objects.create_user(username=email,
                                            email=email,
                                            password = pass1)
            if user is not None:
                user.save()
                user = auth.authenticate(username=email, password=pass1)            
                if user is not None:
                    user_info = UserProfile(user=user)
		    user_info.save()
                    
		    #successful login
                    login(request, user)

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
    
