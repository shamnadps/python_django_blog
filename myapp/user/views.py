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

    def post(self, request, format=None):
        """
        :param request:
        :param format:
        :return:
        """
        username = request.data['username']
        password = request.data['password']
        email = request.data.get('email', None)
        phone = request.data.get('phone', None)
        if SalesTracker_User.objects.filter(phone=phone).exists():
            ERROR_RESP['error']['message'] = USER_ALREADY_EXISTS
            return Response(status=status.HTTP_409_CONFLICT, data=ERROR_RESP)
        else:
            user = SalesTracker_User(username,password, phone, timezone.now(), "active")

        # Building the response
        USER_CREATED['data']['username'] = username
        USER_CREATED['data']['email'] = email
        USER_CREATED['data']['id'] = user.userid
        return Response(status=status.HTTP_201_CREATED, data=USER_CREATED)


