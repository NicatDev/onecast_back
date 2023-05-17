from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model, login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.serializers import ProfileForFilterPageSerializer,UserSerializerForSettingEdit,ProfileSerializerForSettingEdit,AboutMeForRegisterSerializer,UserRegisterSerializer,ProfileSerializer,CompanySerializer,PopularSerializer,ProfileForHomaPageTalentSerializer,ProfileForSingleSerializer
from account.models import *
from rest_framework.views import APIView
from castingapp.filters import ProductFilter
from castingapp.paginations import CustomPagination
User = get_user_model()

# Create your views here.
class LoginView(APIView):
    # permission_classes = [IsCompanyLead]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"sifre ve ya username yanlisdir"})
        login(request, user)
        
        
        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
            
        }
        return Response({"username": username, "tokens": tokens,"userId":user.id}, status=201)



class RegistrationView(APIView):     
    def post(self,request,format=None):
        data=request.data
        image=request.FILES
        userdata = {'username':data.pop('username'),
                    'email':data.pop('email'),
                    'password':data.pop('password')}

        user_serializer = UserRegisterSerializer(data=userdata)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        data.update(image)
        data['user'] = user.id
        profile_serializer = ProfileSerializer(data = data)
        profile_serializer.is_valid(raise_exception=True)
        profile = profile_serializer.save()
        about_me_serializer = AboutMeForRegisterSerializer(data = {"profile":profile.id})
        about_me_serializer.is_valid(raise_exception=True)
        about_me_serializer.save()
        return Response({"Status": "success"}, status=200)
    """eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1NzA3MjM5LCJpYXQiOjE2ODQxNzEyMzksImp0aSI6IjgwNDQzZDI1YTgzMTQ1ZTNiNTA5NmIyMjEzZmEzMGZmIiwidXNlcl9pZCI6MX0.WFpXV-_d7iJZQOu-kOrjGPFI5jitaL16R37XeJsCuhU"""


class CompanyRegisterView(APIView):     
    def post(self,request,format=None):
        data=request.data
        image=request.FILES
        userdata = {'username':data.pop('username'),
                    'email':data.pop('email'),
                    'password':data.pop('password')}

        user_serializer = UserRegisterSerializer(data=userdata)
        user_serializer.is_valid(raise_exception=True)
        user = user_serializer.save()
        data['user'] = user.id
        profile_serializer = CompanySerializer(data = data)
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
        
        return Response({"Status": "success"}, status=200)
#homepage 
class HomePageTalentsView(generics.ListAPIView):
    serializer_class = ProfileForHomaPageTalentSerializer
    
    def get_queryset(self):
        queryset = Profile.objects.filter(is_premium = True)[0:12]
        if queryset.count()<12:
            count = 12-queryset.count()
            queryset2 = Profile.objects.all().order_by('-created_at')
            combinedqueryset = queryset | queryset2[0:count]
            return combinedqueryset
        return queryset
    
#homepage
class HomePagePopularView(generics.ListAPIView):
    serializer_class = PopularSerializer
      
    def get_queryset(self):
        queryset = Popular.objects.filter(is_active=True)   
        return queryset 
#talentssingle
class TalentSingleView(generics.RetrieveAPIView):
    serializer_class = ProfileForSingleSerializer
    queryset = Profile.objects.all()
    lookup_field = 'id'
    
#talentpageview
class TalentPageView(APIView):
    # filter_backends = (DjangoFilterBackend,)
    # filterset_class = ProductFilter
    # pagination_class = CustomPagination
    def get(self):
        queryset = Profile.objects.get(user = self.request.user.id)
        serializer = ProfileForSingleSerializer
        employee = serializer(queryset)
        return Response(employee.data)
    
class TalentModelFilterPage(generics.ListAPIView):
    serialzier_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_visible=True,is_model=True)

class TalentChildFilterPage(generics.ListAPIView):
    serialzier_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_visible=True,is_child=True)

class TalentActorFilterPage(generics.ListAPIView):
    serialzier_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = CustomPagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_visible=True,is_actor=True)
    
#talentpagesettingeditview
class TalentSettingEditView(APIView):
    def put(self):
        user = self.request.user
        
        # if data.get('phone_number') == '':
        #     del data['phone_number']
        
        if 'phone_number' in data:
            if data.get('phone_number') != '':
               number = data.pop('phone_number')
               profile_id = data.pop('profile_id')
               instance = Profile.objects.get(id = profile_id)
               pserializer = ProfileSerializerForSettingEdit(instance,data = {'phone_number':number},partial=True)
               pserializer.is_valid(raise_exception=True)
               pserializer.save()
               
        if 'password' in data:
            if data.get('password') != '':
                password = data.pop('password')
                user.set_password(password)
                user.save()
                
        data = self.request.data
        userinstance = self.request.user
        if 'username' in data:
            if data.get('username') != '':
                userseria = UserSerializerForSettingEdit(userinstance,data={'username':data.get('username')},partial=True)
                userseria.is_valid()
                userseria.save()
        if 'email' in data:
            if data.get('email') != '':
                userseria = UserSerializerForSettingEdit(userinstance,data={'email':data.get('email')},partial=True)
                userseria.is_valid()
                userseria.save()
        return Response({'message':'success'},status=200)
            
