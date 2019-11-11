from django.shortcuts import render
from django.views.generic import TemplateView, FormView, View

class DashView(TemplateView):
    template_name = 'index.html'

class RewardsView(View):
    pass

class CatalogView(View):
    pass

class AnalyticsView(View):
    pass

class EmployessView(View):
    pass

