from django.forms import ModelForm

from dashboard.models import *
from competition.models import *



#for editing the details of a phase from the dashboard
class PhaseForm(ModelForm):

    class Meta:
        model = Phase
        exclude = ("is_judging_enabled","is_deleted",)
