from django.db import models
from datetime import datetime

from competition.models import *


class ActiveStudents(models.Model):

    total = models.IntegerField(default=0)

    is_initialized = models.BooleanField(default=False)

    timestamp = models.DateTimeField(auto_now_add=True)


    class Meta:

        ordering = ['-timestamp']


    def snapshot(self):
        print 'snapshot'

        if self.is_initialized:
            raise Exception("KPI Model Error", "Instance has already been initialized via snapshot(). Please create new instance to save fresh data.")

        #flag to prevent snapshot() from later overriding existing data
        self.is_initialized = True
        self.save()

        date = datetime.now()

        for competition in Competition.objects.all():
            print 'trying competition: %s' % competition
            num = 0
            if Phase.objects.filter(competition=competition).filter(deadline__lte=date).count() > 0:
                num = competition.applicants.count()
                print '  %s applicants' % num

            else:
                print '  not active'

            details = ActiveStudentsFromCompetition(competition=competition, 
                    num=num,
                    snapshot=self)
            details.save()

            self.total += num
            print '  total: %s' % self.total

        self.save()


    def __unicode__(self):

        return u"%s" % self.total


class ActiveStudentsFromCompetition(models.Model):

    competition = models.ForeignKey(Competition)
    snapshot = models.ForeignKey(ActiveStudents)
    num = models.IntegerField()

    
    def __unicode__(self):
        
        return u"%s - %s applicants" % (self.competition, self.num)

