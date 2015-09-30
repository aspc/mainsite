from aspc.menu.models import Menu, MenuSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import SessionAuthentication, BasicAuthentication, TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.throttling import UserRateThrottle

class MenuList(APIView):
    """
    List all menus
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRateThrottle,)

    def get(self, request, format=None):
        menus = Menu.objects.all()
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

class MenuDiningHallDetail(APIView):
    """
    Retrieve a list of menus by their dining hall
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRateThrottle,)

    def get_object(self, dining_hall):
        try:
            return Menu.objects.filter(dining_hall=dining_hall)
        except Menu.DoesNotExist:
            raise Http404

    def get(self, request, dining_hall, format=None):
        menus = self.get_object(dining_hall)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

class MenuDayDetail(APIView):
    """
    Retrieve a list of menus by their day
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRateThrottle,)

    def get_object(self, day):
        try:
            return Menu.objects.filter(day=day)
        except Menu.DoesNotExist:
            raise Http404

    def get(self, request, day, format=None):
        menus = self.get_object(day)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

class MenuDiningHallDayDetail(APIView):
    """
    Retrieve a list of menus by their dining hall and day
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRateThrottle,)

    def get_object(self, dining_hall, day):
        try:
            return Menu.objects.filter(dining_hall=dining_hall).filter(day=day)
        except Menu.DoesNotExist:
            raise Http404

    def get(self, request, dining_hall, day, format=None):
        menus = self.get_object(dining_hall, day)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)

class MenuDiningHallDayMealDetail(APIView):
    """
    Retrieve a menu by its dining hall, day, and meal
    """
    authentication_classes = (SessionAuthentication, BasicAuthentication, TokenAuthentication)
    permission_classes = (IsAuthenticated,)
    throttle_classes = (UserRateThrottle,)

    def get_object(self, dining_hall, day, meal):
        try:
            return Menu.objects.filter(dining_hall=dining_hall).filter(day=day).filter(meal=meal)
        except Menu.DoesNotExist:
            raise Http404

    def get(self, request, dining_hall, day, meal, format=None):
        menus = self.get_object(dining_hall, day, meal)
        serializer = MenuSerializer(menus, many=True)
        return Response(serializer.data)