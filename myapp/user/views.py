__author__ = 'shamnad'

from django.shortcuts import render, get_object_or_404, redirect
from myapp.models import SalesTracker_User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.http import HttpResponse
from myapp.models import Post
from myapp.utils.messages import USER_ALREADY_EXISTS, ERROR_RESP, USER_CREATED, TEST_RESPONSE


class CreateUserView(APIView):

    """
    The view handles the user operations.
    """

    def get(self, request, format=None):
        """
        :param request:
        :param format:
        :return:
        """
        username = request.GET.get('user', None)
        password = request.GET.get('pass', None)
        phone = request.GET.get('phone', None)
        if SalesTracker_User.objects.filter(phone=phone).exists():
            ERROR_RESP['error']['message'] = USER_ALREADY_EXISTS
            return Response(status=status.HTTP_409_CONFLICT, data=ERROR_RESP)
        else:
		
            user = SalesTracker_User(phone,username,password, phone, timezone.now(), 'true');
            user.created_date = timezone.now();
            user.save();

        # Building the response
        USER_CREATED['data']['username'] = username
        USER_CREATED['data']['phone'] = phone
        users = SalesTracker_User.objects.filter(created_date__lte=timezone.now()).values()
        return Response(status=status.HTTP_201_CREATED, data=users)


