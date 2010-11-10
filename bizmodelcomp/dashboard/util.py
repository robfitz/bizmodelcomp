from competition.models import Competition

#permissions helper
def has_dash_perms(request, competition_id):

    if not request.user.is_authenticated():
        return False

    try:
        competition = Competition.objects.get(id=competition_id)
        return competition.owner == request.user
    
    except:
        return False
    
    return False
