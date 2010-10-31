from random import Random
import string


#return a randomized alphanumerical string with a
#number of characters equal to length
def rand_key(length=12):
    
    return ''.join([choice(string.letters+string.digits) for i in range(length)])
