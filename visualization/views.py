from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .models import Codes, MonthSafetyCntView, NormalSFView, HgvCntView

from django.db.models import Count
from django.db.models.functions import ExtractMonth
from .dash import app


def model_view(request):
    return render(request, "visualization/statistics.html")