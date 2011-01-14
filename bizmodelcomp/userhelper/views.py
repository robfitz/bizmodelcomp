from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth import *
from django.contrib.auth.models import User

from settings import ACCOUNT_EMAIL_CONFIRM_REQUIRED
from userhelper.util import *
from userhelper.models import *
from judge.models import *
from utils.util import rand_key

from competition.models import *



def account_settings(request):

    alert = None

    if request.method == "POST":

        name = request.POST.get("name")
        email = request.POST.get("email_1")
        email_2 = request.POST.get("email_2")

        if email and email != email_2:
            alert = "The email addresses you entered didn't match. Please try again."

        elif email and email == email_2:
            #change email address
            request.user.email = email
            request.user.save()

        if name:
            #change name
            try:
                request.user.first_name = name
                request.user.save()

            except:
                alert = "%s" % sys.exc_info()[0]

        if not alert:
            #no alert means success
            return HttpResponseRedirect('/dashboard/')

        else:
            #failure of some kind, show a message
            return render_to_response('userhelper/account_settings.html', locals())

    return render_to_response('userhelper/account_settings.html', locals())



def noPermissions(request):

    return render_to_response('userhelper/no_permissions.html')



def loginRegister(request):

    if request.user.is_authenticated():
        return HttpResponseRedirect('/dashboard/')

    alert = None
    alert = "Sorry, registration is currently disabled. We'll be opening to the public soon!"

    if request.method == "POST" and len(request.POST) > 0:
        pass

    if False == True:
        
        login_or_register = request.POST.get("login_or_register", "login")

        if login_or_register == "login":

            email = request.POST.get("email", None)
            password = request.POST.get("password", None)
            username = None

            try:
                email_user = User.objects.get(email=email)
                username = email_user.username
            except:
                alert = "We couldn't find a user with that email. Typo? Please try again or create a new account if you don't yet have one."

                return render_to_response('userhelper/login_register.html', locals())


            user = auth.authenticate(username=username, password=password)

            if user is not None:

                print 'user is not none! %s, %s' % (request, user)

                #logged in successfully
                auth.login(request, user)

                next = request.POST.get("next", None)
                print 'got next: %s' % next

                if not next:

                    print 'length of judge invitations: %s' % JudgeInvitation.objects.filter(user=user)

                    next = "/dashboard/"
                
                return HttpResponseRedirect(next)
            
            else:
                #login failed
                alert = "Login failed. Try again?"


        elif login_or_register == "register":

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

                next = request.POST.get("next", "/dashboard")

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
        next = request.GET.get("next", None)

        email = request.GET.get("e", "")

        #if they got to the judging page from the email link,
        #we can verify their email right now
        got_ev_key(request.GET.get("ev", False))
                
    return render_to_response('userhelper/login_register.html', locals())



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

            next = request.POST.get("next", None)
            print 'got next: %s' % next

            if not next:

                print 'length of judge invitations: %s' % JudgeInvitation.objects.filter(user=user)

                next = "/dashboard/"
            
            return HttpResponseRedirect(next)
        
        else:
            #login failed
            alert = "Login failed. Try again?"

    elif request.method == "GET":
        #page to redirect to after success
        next = request.GET.get("next", None)

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

            next = request.POST.get("next", "/dashboard/")

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
    
