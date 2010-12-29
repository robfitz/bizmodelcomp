from django.db import models



class BlogPost(models.Model):

    url = models.CharField(max_length=200, unique=True, primary_key=True)

    #BlogPost.title is based off of BlogPost.url, which customer_title lets you override 
    custom_title = models.CharField(max_length=200)

    #if True, hides blog post in main view but still allows access via direct url
    is_draft = models.BooleanField(default=False)

    #contents
    text = models.CharField(max_length=10000)

    #timestamp
    created = models.DateTimeField(auto_now_add=True)


    def title(self):

        if self.custom_title:
            return self.custom_title

        else:
            #capitalize first character
            default_title = "%s%s" % (upper(self.url[0]), self.url[1:])

            #sub in spaces for dashes
            default_title = replace(default_title, '-', ' ')
            default_title = replace(default_title, '_', ' ')

            return default_title

            




