from django import template
from django.template.defaultfilters import stringfilter

register = template.Library()


@stringfilter
def max_chars(value, arg):

    value = value.strip()
    num_chars = 0
    try:
        num_chars = int(arg)
    except:
        return value

    if num_chars <= 0:
        return value 

    if len(value) <= num_chars:
        return value

    words = value.split(' ')
    if len(words) <= 1 or len(words[0]) > num_chars:
        return "%s..." % value[:num_chars]

    else:
        #more than one word, return words until next word would exceed length
        truncated = "" 
        for w in words:
            if len("%s %s" % (truncated, w)) > num_chars:
                return "%s..." % truncated
            else:
                truncated = "%s %s" % (truncated, w)

    return value


register.filter("max_chars", max_chars)
