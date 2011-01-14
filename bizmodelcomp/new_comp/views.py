from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response
from django.contrib import auth
from django.contrib.auth import *
import sys

from utils.util import rand_key
from utils.models import Tag
from competition.models import Competition, Phase

from userhelper.models import *
from userhelper.views import createNewUser, is_new_user_judge

from settings import ACCOUNT_EMAIL_CONFIRM_REQUIRED


def new(request):

    owner = None
    if request.user.is_authenticated:
        competition = Competition(name="New competition",
                hosted_url = rand_key(),
                owner=owner)
    else:
        competition = Competition(name="New competition",
                hosted_url = rand_key())

    competition.save()

    request.session["new_comp_id"] = competition.id

    return HttpResponseRedirect("/new/who/")



APPLICANT_TYPES = ["undergrad", "postgrad", "faculty", "nonacademic"]
BUSINESS_TYPES = ["web", "social", "green", "medical", "services", "other-ideas"]


def get_tag(name):

    try:
        return Tag.objects.get(name=name)
    except:
        tag = Tag(name=name)
        tag.save()
        return tag



def who(request):

    #try grabbing the competition-in-progress from their session
    competition = None
    try:
        competition = Competition.objects.get(id=request.session["new_comp_id"])
    except:
        return HttpResponseRedirect("/new/")

    print '### new: setting up who on comp: %s' % competition.id

    if request.method == "POST":

        reqs = competition.application_requirements()

        #completely overwrite all existing tags
        reqs.remove_all()

        #TODO NEXT: test that these tags get added & removed properly after submit

        for key in request.POST:

            print 'checking key: %s' % key
            value = request.POST.get(key)

            if value is not None:

                value = value.strip()
                if value:

                    toks = key.split("_")
                    if key.startswith("location_"):
                        reqs.locations.add(get_tag(request.POST.get(key)))
                        print 'added to location: %s' %request.POST.get(key)

                    elif key.startswith("other-requirements_"):
                        reqs.other_requirements.add(get_tag(request.POST.get(key)))
                        print 'added to other reqs: %s' %request.POST.get(key)

                    elif key.startswith("other-ideas_"):
                        reqs.business_types.add(get_tag(request.POST.get(key)))
                        print 'added to other ideas: %s' %request.POST.get(key)

                    elif key.startswith("institution_"):
                        reqs.institutions.add(get_tag(request.POST.get(key)))
                        print 'added to institution: %s' %request.POST.get(key)

        #a couple traits are special cased because they're added free-form
        #and this makes them agree with our processing of standard tags
        #if request.POST.get("institutions"):
            #list = request.POST.get("institutions").split(";")
            #custom_tag_data.append( ( list, reqs.institutions) )
        #else:
            #custom_tag_data.append( ( [], reqs.institutions ) )
#
        #if request.POST.get("locations"):
            #location_list = request.POST.get("locations").split(";")
            #custom_tag_data.append( ( location_list, reqs.locations) )
        #else:
            #custom_tag_data.append( ( [], reqs.locations ) )

        #if request.POST.get("other-requirements"):
            #other_requirement_list = request.POST.get("other-requirements").split(";")
            #custom_tag_data.append( ( other_requirement_list, reqs.other-requirements) )
        #else:
            #custom_tag_data.append( ( [], reqs.other-requirements ) )

        #for tag_names, current_tags in custom_tag_data:
            #for tag in current_tags.all():
                #current_tags.remove(tag)
#
            #for tag_name in tag_names:
                #try:
                    #current_tags.add(Tag.objects.get(name=tag_name))
                #except:
                    #tag = Tag(name=tag_name)
                    #tag.save()
                    #reqs.add(tag)

        tag_data = [ ( APPLICANT_TYPES, reqs.applicant_types),
                     ( BUSINESS_TYPES, reqs.business_types) ]

        #add/remove a couple different sets of tags
        for tag_names, current_tags in tag_data:

            print 'tag names: %s' % tag_names

            #checking each tag within each set
            for tag_name in tag_names:
                print 'testing tag name: %s' % tag_name

                #is tag desired?
                if request.POST.get(tag_name):

                    print 'turn on tag: %s' % tag_name
                    try:
                        #if tag exists on another comp, 
                        #we add it to this one also
                        current_tags.add(Tag.objects.get(name=tag_name))
                        print 'added existing tag: %s' % tag
                    except:
                        #otherwise, we'll create it
                        tag = Tag(name=tag_name)
                        tag.save()
                        current_tags.add(tag)
                        print 'added new tag: %s' % tag

        return HttpResponseRedirect("/new/phases/")

    return render_to_response("new_comp/who.html", locals())



def phase_structure(request):

    #try grabbing the competition-in-progress from their session
    competition = None
    try:
        competition = Competition.objects.get(id=request.session["new_comp_id"])
    except:
        return HttpResponseRedirect("/new/")

    print '### new: setting up phases on comp: %s' % competition.id

    if request.method == "POST":

        print "POST: %s" % request.POST

        max_num = 0
        for key in request.POST:

            print 'checking key: %s' % key

            if key.startswith("live_") or key.startswith("online_"):
                num = int(key.split("_")[1])
                if num > max_num:
                    max_num = num
                    print 'max num set to: %s' % max_num

        for i in range(0, max_num + 1):

            pitch_type = None
            if request.POST.get("online_%s" % i):
                pitch_type = "online"
            elif request.POST.get("live_%s" % i):
                pitch_type = "live"

            print 'pitch type: %s' % pitch_type
                
            if pitch_type is not None:

                print 'for %s_%s' % (pitch_type, i)
                #add a live phase    
                new_phase = Phase(competition=competition,
                        name=request.POST.get("%s_%s" % (pitch_type, i)),
                        pitch_type=pitch_type)
                new_phase.save()

                print 'added new phase: %s with pitch type: %s' % (new_phase, pitch_type)

        if Phase.objects.filter(competition=competition).count() > 0:
            #success, added at least one phase, so set first one as
            #current and move on 
            competition.current_phase = Phase.objects.filter(competition=competition)[0]
            competition.save()
            return HttpResponseRedirect("/new/details/")

        else:
            alert = "You need to add at least one phase to your competition before continuing"

    return render_to_response("new_comp/phase_structure.html", locals())



def competition_details(request):

    #try grabbing the competition-in-progress from their session
    competition = None
    try:
        competition = Competition.objects.get(id=request.session["new_comp_id"])
    except:
        return HttpResponseRedirect("/new/")

    print '### new: setting details on comp: %s' % competition.id

    if request.method == "POST":

        alert = None

        hosted_url = request.POST.get("hosted_url")
        name = request.POST.get("name")
        prize_money = request.POST.get("prize_money")
        other_prizes = request.POST.get("other_prizes")

        if not hosted_url or not name:
            alert = "The name and URL fields are required. Please choose what you'd like to call it and try again."

        try:
            competition.hosted_url = hosted_url
            competition.name = name
            competition.save()

        except:
            #data validation problem
            alert = "That competition URL has already been used. Please try something different."

        if alert is not None:
            return render_to_response("new_comp/comp_details.html", locals())

        elif not request.user.is_authenticated():
            #done setting up comp, but they still need a username & pw
            return HttpResponseRedirect("/new/register/")

        else:
            #all done, go to their dashboard for their new comp
            return HttpResponseRedirect("/dashboard/")

    return render_to_response("new_comp/comp_details.html", locals())


def login(request):

    #try grabbing the competition-in-progress from their session
    competition = None
    try:
        competition = Competition.objects.get(id=request.session["new_comp_id"])
    except:
        return HttpResponseRedirect("/new/")

    print '### new: logging in on comp: %s' % competition.id

    override_register_url = "/new/register/"

    if request.method == "POST":

            email = request.POST.get("email", None)
            password = request.POST.get("password", None)
            username = None

            try:
                email_user = User.objects.get(email=email)
                username = email_user.username
            except:
                alert = "We couldn't find a user with that email. Typo? Please try again or create a new account if you don't yet have one."

                return render_to_response('userhelper/login.html', locals())

            user = auth.authenticate(username=username, password=password)

            if user is not None:

                print 'user is not none! %s, %s' % (request, user)

                #logged in successfully
                auth.login(request, user)

                competition.owner = user
                competition.save()

                next = request.POST.get("next", "/dashboard/")

                return HttpResponseRedirect(next)
            
            else:
                #login failed
                alert = "Login failed. Try again?"

    alert = "Please register or log in so we can save your competition for you."

    return render_to_response("userhelper/login.html", locals())

def register(request):

    alert = "Sorry, registration is currently disabled. We'll be opening to the public soon!"

    override_login_url = "/new/login/"

    #try grabbing the competition-in-progress from their session
    competition = None
    try:
        competition = Competition.objects.get(id=request.session["new_comp_id"])
    except:
        return HttpResponseRedirect("/new/")

    print '### new: registering on comp: %s' % competition.id

    if request.method == "POST":

        pass

    if False == True:

            email = request.POST["email"]
            pass1 = request.POST["password1"]
            pass2 = request.POST["password2"]
                
            user = None
            try:
                user = createNewUser(request, email, pass1, pass2)
                competition.owner = user
                competition.save()
                
            except:
                next = request.POST.get("next")
                login = "/new/login/"
                if next:
                    login += "?next=%s" % next
                alert = "That email has already been registered. Try <a href='%s'>logging in</a> instead?" % login
                print sys.exc_info()[0]

            try:
                #is there a verification key already hooked up to that email?
                key = VerificationKey.objects.get(email=user.email)
                key.user = user
                key.save()
            except: pass

            if user is not None:

                is_judge = is_new_user_judge(user)
                print 'so was it a judge? %s' % is_judge

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


    alert = "Please register or log in so we can save your competition for you."

    return render_to_response("userhelper/register.html", locals())



