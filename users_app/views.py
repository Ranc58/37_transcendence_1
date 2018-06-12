from django.views import generic
from django.contrib.auth.models import User


class UsersView(generic.DetailView):
    model = User
    template_name = 'user.html'
