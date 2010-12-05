from django.forms import ModelForm

from dashboard.models import *
from competition.models import *



class CompetitionInfoForm(ModelForm):

    class Meta:
        model = Competition
        fields = ("name",
                "website",
                "hosted_url",
                "logo")

#for editing the details of a phase from the dashboard
class PhaseForm(ModelForm):

    class Meta:
        model = Phase
        exclude = ("is_judging_enabled",
                   "is_deleted",
                   "current_status",
                   "min_judgements_per_pitch",
                   "deadline")
