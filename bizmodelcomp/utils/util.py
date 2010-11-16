from random import choice
import string


#return a randomized alphanumerical string with a
#number of characters equal to length
def rand_key(length=12):
    print 'xxx rand_key'
    built = ''.join([choice(string.letters+string.digits) for i in range(length)])
    print 'xxx = %s' % built
    return built


def ordinal(n):
	"""borrowed from John Machin's python-list post.  Appends an
	ordinal suffix to a number.  For example, 1 becomes 1st,
	2 becomes 2nd, etc."""
	if 10 <= n % 100 < 20:
		return str(n) + 'th'
	else:
		return  str(n) + {1 : 'st', 2 : 'nd', 3 : 'rd'}.get(n % 10, "th")
