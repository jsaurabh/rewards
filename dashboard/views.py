from django.shortcuts import render
from django.views.generic import TemplateView

# Create your views here.
# def home(request):
#     return HttpResponse("Hello, World!")

class DashView(TemplateView):
    template_name = 'index.html'

# class EmptyView(TemplateView):
#     template_name = 'blank.html'