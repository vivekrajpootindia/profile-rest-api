from django.shortcuts import render

from rest_framework import viewsets
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.authentication import TokenAuthentication
from rest_framework import filters
from rest_framework.authtoken.serializers import AuthTokenSerializer
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework.permissions import IsAuthenticated

from . import serilizer

from . import models
from .import permission

# Create your views here.


class HellowApiView(APIView):
    # testing api view

    serializer_class = serilizer.FirstSerilizer

    def get(self,request,format=None):
        # return list of view

        api_view = ['list of api','second pointer']

        return Response({'message':'HellowApi','list':api_view})

    def post(self, request):
        # post request

        seriliz = serilizer.FirstSerilizer(data = request.data)

        if seriliz.is_valid():
            name = seriliz.data.get('name')
            message = 'Hi {}'.format(name)
            return Response({'message':message})
        else:
            return Response(seriliz.errors,status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk=None):
        # updating the object
        return Response({'message':'put'})

    def patch(self, request, pk=None):
        # partialy update the object the field provided in the request
        return Response({'message':'patch'})

    def delete(self, request, pk=None):
        # deleting the object
        return Response({'message':'delete'})

class HelloApiViewSet(viewsets.ViewSet):
    # performing CRUD interface oprations

    serializer_class = serilizer.FirstSerilizer
    def list(self, request):
        view_set = ['first view set','with list return']

        return Response({'message':'view set','list':view_set})

    def create(self, request):
        # creating the new entry
        seri = serilizer.FirstSerilizer(data = request.data)

        if seri.is_valid():
            name = seri.data.get('name')
            return Response({'message':'Hi','name':name})
        else:
            return Response(seri.errors, status=status.HTTP_400_BAD_REQUEST)

    def retrieve(self, request, pk=None):
        # return retrieve message
        return Response({'message':'get','data':pk})

    def update(self, request, pk=None):
        return Response({'message':'put','data':pk})

    def partial_update(self, request, pk=None):
        # handle partialy update the objects
        return Response({'message':'patch','data':pk})

    def destroy(self, request, pk=None):
        # delete the object
        return Response({'message':'delete','data':pk})

class UserProfileViewSet(viewsets.ModelViewSet):
    # create read update profile

    serializer_class = serilizer.UserProfileSerializer
    queryset = models.UserProfile.objects.all()

    authentication_classes = (TokenAuthentication, )
    permission_classes = (permission.UpdateOwnProfile,)
    filter_backends = (filters.SearchFilter,)
    search_fields = ('name', 'email',)


class LoginViewSet(viewsets.ViewSet):
    # check email and password and return AuthoToken

    serializer_class = AuthTokenSerializer

    def create(self, request):
        # use to obtain token view and validate

        return ObtainAuthToken().post(request)

class ProfileFeedViewSet(viewsets.ModelViewSet):
    # create read and update feed item`
    authentication_classes = (TokenAuthentication, )
    serializer_class = serilizer.ProfileFeedItemSerializer
    queryset = models.ProfileFeedItem.objects.all()
    permission_classes = (permission.PostOwnStatus, IsAuthenticated)


    def perform_create(self, serilizer):
        # set the user profile to the logged in user
        serilizer.save(user_profile=self.request.user)
