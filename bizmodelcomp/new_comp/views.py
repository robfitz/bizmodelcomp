from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response

from utils.util import rand_key
from utils.models import Tag
from competition.models import Competition, Phase


def new(request):

    competition = Competition(name="New competition",
            hosted_url = rand_key(),
            owner=request.user #probably still anonymous, will update this later
            )
    competition.save()

    request.session["new_comp_id"] = competition.id

    return HttpResponseRedirect("/new/who/")



APPLICANT_TYPES = ["undergrad", "postgrad", "faculty", "nonacademic"]
BUSINESS_TYPES = ["web", "social", "green", "medical", "services", "other_ideas"]

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

        custom_tag_data = []

        #a couple traits are special cased because they're added free-form
        #and this makes them agree with our processing of standard tags
        if request.POST.get("institutions"):
            list = request.POST.get("institutions").split(";")
            custom_tag_data.append( ( list, reqs.institutions) )
        else:
            custom_tag_data.append( ( [], reqs.institutions ) )

        if request.POST.get("locations"):
            location_list = request.POST.get("locations").split(";")
            custom_tag_data.append( ( location_list, reqs.locations) )
        else:
            custom_tag_data.append( ( [], reqs.locations ) )

        #if request.POST.get("other_requirements"):
            #other_requirement_list = request.POST.get("other_requirements").split(";")
            #custom_tag_data.append( ( other_requirement_list, reqs.other_requirements) )
        #else:
            #custom_tag_data.append( ( [], reqs.other_requirements ) )

        for tag_names, current_tags in custom_tag_data:
            for tag in current_tags.all():
                current_tags.remove(tag)

            for tag_name in tag_names:
                try:
                    current_tags.add(Tag.objects.get(name=tag_name))
                except:
                    tag = Tag(name=tag_name)
                    tag.save()
                    reqs.add(tag)

        tag_data = [ ( APPLICANT_TYPES, reqs.applicant_types),
                     ( BUSINESS_TYPES, reqs.business_types) ]

        #add/remove a couple different sets of tags
        for tag_names, current_tags in tag_data:

            print 'tag names: %s' % tag_names

            #clear existing ones so we can just add new ones
            for tag in current_tags.all():
                current_tags.remove(tag)

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

            if key.startswith("live_") or key.startswith("online_"):
                num = int(key.split("_")[1])
                if num > max_num:
                    max_num = num

        for i in range(0, max_num):

            pitch_type = None
            if request.POST.get("online_%s" % i):
                pitch_type = "online"
            elif request.POST.get("live_%s" % i):
                pitch_type = "live"
                
            if pitch_type is not None:

                print 'for %s_%s' % (pitch_type, i)
                #add a live phase    
                new_phase = Phase(competition=competition,
                        name=request.POST.get("%s_%s" % (pitch_type, i)),
                        pitch_type=pitch_type)
                new_phase.save()

                print 'added new phase: %s with pitch type: %s' % (new_phase, pitch_type)

        return HttpResponseRedirect("/new/details/")

    return render_to_response("new_comp/phase_structure.html", locals())



def competition_details(request):

    if request.method == "POST":

        if not request.user.is_authenticated():

            return HttpResponseRedirect("/new/register/")

        else:

            #save competition
            pass

        return HttpResponseRedirect("/new/details/")

    return render_to_response("new_comp/comp_details.html", locals())



def register(request):

    return render_to_response("userhelper/login_register.html", locals())
