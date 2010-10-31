from random import choice
import string


#return a randomized alphanumerical string with a
#number of characters equal to length
def rand_key(length=12):
    print 'xxx rand_key'
    built = ''.join([choice(string.letters+string.digits) for i in range(length)])
    print 'xxx = %s' % built
    return built
