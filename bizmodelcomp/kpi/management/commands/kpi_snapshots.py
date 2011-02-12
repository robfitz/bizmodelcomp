from django.core.management.base import BaseCommand, CommandError

from kpi.models import *


class Command(BaseCommand):

    args = ''
    help = 'Takes a snapshot of the various metrics to save as KPI models for display on the business dashboard'

    def handle(self, *args, **options):

        active_students = ActiveStudents()
        active_students.save()
        active_students.snapshot()






