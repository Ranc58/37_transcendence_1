from django.http import HttpResponse, HttpResponseNotFound
from django.views import View
from django.contrib.auth.models import User
from raven.contrib.django.raven_compat.models import client as raven_client


class UsersView(View):

    def get(self, request, user_id):
        try:
            current_user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            raven_client.captureException()
            return HttpResponseNotFound(content='User not found')
        user_info = "Username: {}<br> First name: {}<br> Last name: {}<br> Email: {}".format(
            current_user.username,
            current_user.first_name if current_user.first_name else 'Not avaliable',
            current_user.last_name if current_user.last_name else 'Not avaliable',
            current_user.email if current_user.email else 'Not avaliable'
        )
        return HttpResponse(content=user_info)
