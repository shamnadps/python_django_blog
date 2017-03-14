__author__ = 'shamnad'

from django.shortcuts import render, get_object_or_404, redirect
from myapp.models import SalesTracker_User
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from django.utils import timezone
from django.http import HttpResponse
from myapp.models import Post
from myapp.utils.messages import USER_ALREADY_EXISTS, ERROR_RESP, USER_CREATED,TEST_RESPONSE


class CreateTestView(APIView):

        """
        This is to test api call.
        """

        def get(self, request, format=None):
            return Response(status=status.HTTP_201_CREATED, data=TEST_RESPONSE)

