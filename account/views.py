from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model, login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.serializers import ProfileImageSerializer,About_me_edit_Serializer,ChangePasswordSerializer,CompanyListSerializer,ProfileForFilterPageSerializer,UserSerializerForSettingEdit,ProfileSerializerForSettingEdit,AboutMeForRegisterSerializer,UserRegisterSerializer,ProfileSerializer,CompanySerializer,PopularSerializer,ProfileForHomaPageTalentSerializer,ProfileForSingleSerializer
from account.models import *
from rest_framework.views import APIView
from castingapp.filters import ProductFilter
from castingapp.paginations import Custom9Pagination,Custom12Pagination
from django.contrib.auth.hashers import check_password
User = get_user_model()

# Create your views here.
class TalentLoginView(APIView):
    # permission_classes = [IsCompanyLead]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"sifre ve ya username yanlisdir"},status=400)

        if Company.objects.filter(user=user.id):
            roles = [2002]
        elif Profile.objects.filter(user=user.id):   
            roles = [2000]
        else:
            roles = [2023]
        login(request, user)    
        
        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        
        return Response({"username": username, "tokens": tokens,"roles":roles}, status=201)

class CompanyLoginView(APIView):
    # permission_classes = [IsCompanyLead]
    def post(self, request, *args, **kwargs):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if not user:
            return Response({"sifre ve ya username yanlisdir"})
        if Profile.objects.filter(user=user.id):
            return Response({'Bu parametrlerde hesab movcud deyil'})
        if Company.objects.filter(user=user.id):   
            roles = [2002] 
            login(request, user)
        
        
        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        
        return Response({"username": username, "tokens": tokens,"roles":roles}, status=201)




class RegistrationView(APIView):     
    def post(self,request,format=None):
        data=request.data

        userdata = {'username':data.pop('username')[0],
                    'email':data.pop('email')[0],
                    'password':data.pop('password')[0]}
        if data.get('fullname'):
            first_name, last_name = data.pop('fullname')[0].split()
            data['first_name'] = first_name
            data['last_name'] = last_name
        user_serializer = UserRegisterSerializer(data=userdata)
        if user_serializer.is_valid():
            user = user_serializer.save()

            data['user'] = user.id
            profile_serializer = ProfileSerializer(data = data)
            if profile_serializer.is_valid():
                profile = profile_serializer.save()
                about_me_serializer = AboutMeForRegisterSerializer(data = {"profile":profile.id})
                about_me_serializer.is_valid(raise_exception=True)
                about_me_serializer.save()
            else:
                print(profile_serializer.errors)
                return Response({'Status':profile_serializer.errors,'error':'profile'},status=400)
        else:
            print(user_serializer.errors)
            return Response ({'Status':user_serializer.errors,'error':'user'},status=401)
        return Response({"Status": "success","id":profile.id}, status=200)
    """eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzE1NzA3MjM5LCJpYXQiOjE2ODQxNzEyMzksImp0aSI6IjgwNDQzZDI1YTgzMTQ1ZTNiNTA5NmIyMjEzZmEzMGZmIiwidXNlcl9pZCI6MX0.WFpXV-_d7iJZQOu-kOrjGPFI5jitaL16R37XeJsCuhU"""


class CompanyRegisterView(APIView):     
    def post(self,request,format=None):
        data=request.data

        userdata = {'username':data.pop('username')[0],
                    'email':data.pop('email')[0],
                    'password':data.pop('password')[0]}

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

    def get(self,request):
        
        queryset = Profile.objects.get(user = self.request.user.id)
        serializer = ProfileForSingleSerializer
        employee = serializer(queryset)
        return Response(employee.data)
    
class TalentModelFilterPage(generics.ListAPIView):
    serializer_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = Custom9Pagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_visible=True,is_model=True)

class TalentChildFilterPage(generics.ListAPIView):
    serializer_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = Custom9Pagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_visible=True,is_child=True)

class TalentActorFilterPage(generics.ListAPIView):
    serializer_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = Custom9Pagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_visible=True,is_actor=True)
    
class TalentAllFilterPage(generics.ListAPIView):
    serializer_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = Custom12Pagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_visible=True)

class TalentFilterPage(generics.ListAPIView):
    serializer_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = Custom9Pagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_visible=True)
    
class CompanyListView(generics.ListAPIView):
    serializer_class = CompanyListSerializer 
    queryset = Company.objects.all()
    # pagination_class = Custom12Pagination
    
#talentpagesettingeditview
class TalentSettingEditView(APIView):
    def put(self,request):
        # user = self.request.user
        data=request.data
        number = data.pop('phone_number')
        first_name = data.pop('first_name')
        last_name = data.pop('last_name')
        profile_id = data.pop('profile_id')
        instance = Profile.objects.get(id = profile_id)
        pserializer = ProfileSerializerForSettingEdit(instance,data = {'phone_number':number,'first_name':first_name,'last_name':last_name},partial=True)
        pserializer.is_valid(raise_exception=True)
        pserializer.save()
               

        userinstance = request.user

        userseria = UserSerializerForSettingEdit(userinstance,data=data,partial=True)
        userseria.is_valid()
        userseria.save()

        return Response({'message':'success'},status=200)
            
class CheckUsername(APIView):
    def post(self,request):
        username = self.request.data.get('username')
        email = self.request.data.get('email')
        if User.objects.filter(username=username).exists() and User.objects.filter(email=email).exists():
            return Response({"email":"false","username":"false"},status=400)
        elif User.objects.filter(username=username).exists():
            return Response({"email":"true","username":"false"},status=400)
        elif User.objects.filter(email=email).exists():
            return Response({"email":"false","username":"true"},status=400)
        
        return Response({"email":"true","username":"true"},status=200)
    
    
class ChangePasswordVerifyView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = ChangePasswordSerializer
    lookup_field = "id"
            
        
    def put(self, request, *args, **kwargs):
        obj = self.get_object()
        serializer = self.serializer_class(data=request.data,instance=obj)
        
        serializer.is_valid(raise_exception=True)
        if obj.check_password(serializer.validated_data['expassword']):
                return Response({"error": "Parol doğru değil."}, status=400)
        serializer.save()
        return Response({'Status':'Success'}, status=201)
    
class AboutMeEditView(APIView):
    queryset = About_me.objects.all()
    
    def put(self,request,*args,**kwargs):
        data = self.request.data
        instance = About_me.objects.get(id = data.pop("id"))
        languages = []
        for x in data.pop('languages'):
            item = Languages.objects.get(name=x)
            languages.append(item)
        about_me_serializer = About_me_edit_Serializer(instance,data,partial=True)
        about_me_serializer.is_valid(raise_exception=True)
        
        my_about_me = about_me_serializer.save()
        


        my_about_me.language.set(languages)
        my_about_me.save()
        return Response({"message":"success"},status=200)
        
# {"content":"1","facebook":"1","linkedn":"1","instagram":"1","languages":["Tr","Eng","Rus"],"id":1}

class ProfileImageEdit(generics.UpdateAPIView):
    queryset = Profile.objects.all()
    serializer_class = ProfileImageSerializer
    lookup_field = 1
    

class CategoryEditView(APIView):
    queryset = Profile.objects.all()
    
    def put(self,request,*args,**kwargs):
        data = self.request.data
        instance = Profile.objects.get(id = data.pop("id"))
        actor_cat = []
        model_cat = []
        for x in data.pop('model_cat'):
            item = ModelCategory.objects.get(name=x)
            model_cat.append(item)
        for x in data.pop('actor_cat'):
            item = ActorCategory.objects.get(name=x)
            actor_cat.append(item)

        instance.modelCategory.set(model_cat)
        instance.actorCategory.set(actor_cat)
        instance.save()
        return Response({"message":"success"},status=200)
    
# {"id":1,"actor_cat":["Bas rol"],"model_cat":["Top models","Face models"]}

class GetPremiumOrBasic(APIView):
    def put(self,request,*args,**kwargs):
        data = self.request.data
        id = data.get("id")
        profile = Profile.objects.get(id= id)
        profile.is_premium = data.get("is_premium")
        profile.save()
        return Response({"message":"success"},status=200)