from django.shortcuts import render
from django.views.generic import TemplateView, FormView

# Create your views here.
# def home(request):
#     return HttpResponse("Hello, World!")

class DashView(TemplateView):
    template_name = 'index.html'

# def register_view(request):
#     form = UsersRegistrationForm(request.POST or None)
#     if form.is_valid():
#         return redirect("/")
#     print("TO DO")

#     return render(request, "accounts/register.html")