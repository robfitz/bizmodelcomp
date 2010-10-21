from django.db import models
import markdown

from competition.models import Competition
from sitecopy.models import CustomCopy, CustomCopyTemplate


#returns the text of the requested customizable copy blurb
def get_custom_copy(title, competition=None):

    copy = None
    try:
        copy = CustomCopy.objects.filter(title=title).get(competition=competition)
        return copy.text
    except:
        copy = CustomCopyTemplate.objects.get(title=title)
        return copy.default_text

    return "Missing copy for %s" % title    


