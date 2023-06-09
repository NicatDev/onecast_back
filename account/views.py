from django.shortcuts import render
from rest_framework import generics
from rest_framework.response import Response
from django_filters.rest_framework import DjangoFilterBackend
from django.contrib.auth import get_user_model, login, authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from account.serializers import FilterCompanySerializer,FilterProfileSerializer,CompanyImageSerializer,CompanyForSingleSerializer,CompanySerializerForEdit,CompanySerializerForSettingEdit,ModelCategoryListSerializer,ActorCategoryListSerializer,ProfileImageSerializer,About_me_edit_Serializer,ChangePasswordSerializer,CompanyListSerializer,ProfileForFilterPageSerializer,UserSerializerForSettingEdit,ProfileSerializerForSettingEdit,AboutMeForRegisterSerializer,UserRegisterSerializer,ProfileSerializer,CompanySerializer,PopularSerializer,ProfileForHomaPageTalentSerializer,ProfileForSingleSerializer
from account.models import *
from rest_framework.views import APIView
from castingapp.filters import ProductFilter
from castingapp.paginations import Custom9Pagination,Custom12Pagination
from django.contrib.auth.hashers import check_password
from django.db.models import Q
from django.core.mail import send_mail
from django.conf import settings
from django.core.mail import EmailMessage
User = get_user_model()

class CheckLogin(APIView):
    def post(self, request):
        try:
            user = self.request.user
            if User.objects.filter(id = user.id).exists():
                print(user,'200')
                return Response(status=200)
            else:
                return Response(status=400)
        except:
            print(user,'400')
            return Response(status=400)
        return Response(status=401)

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
            return Response({'Bu parametrlerde hesab movcud deyil'},status=401)
        elif Profile.objects.filter(user=user.id):   
            roles = [2000]
        else:
            roles = [2023]
        login(request, user)    
        
        emp = Profile.objects.get(user=user)
        # send_mail(
        #     'Login edildi',
        #     emp.image1,
        #     settings.EMAIL_HOST_USER,
        #     ("nicat254memmedov@gmail.com",),
        #     fail_silently=False,
        # )
        
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
            return Response({"sifre ve ya username yanlisdir"},status=400)
        if Profile.objects.filter(user=user.id):
            return Response({'Bu parametrlerde hesab movcud deyil'},status=401)
        if Company.objects.filter(user=user.id):   
            roles = [2002] 
            login(request, user)
        
        
        refresh = RefreshToken.for_user(user)
        tokens = {
            "refresh": str(refresh),
            "access": str(refresh.access_token)
        }
        
        return Response({"username": username, "tokens": tokens,"roles":roles}, status=201)
"""

{"full_name":"asdasd asdas","username":"asdssssss","password":"123123","phone_number":"1231231","eyecolor":"Sari","weight":12,"gender":"Male","haircolor":"SAri","height":12,"education":"asa"}"""

class RegistrationView(APIView):     
    def post(self,request,format=None):

        data=request.data
        print(data)

        userdata = {'username':data.pop('username')[0],
                    'email':data.pop('email')[0],
                    'password':data.pop('password')[0],
                    'is_active':False}
    
        if data.get('fullname')[0]:
            print(data.get('fullname'),data.get('fullname')[0],'---------------------------')
            first_name, last_name = data.pop('fullname')[0].split()
            
            data['first_name'] = first_name

            data['last_name'] = last_name
            data['is_active'] = True
            data['is_visible'] = True
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
                send_mail(
            'Yeni model ve ya aktyor',
            f"{data['first_name']} {data['last_name']} adli user qeydiyyatdan kecdi !",
            settings.EMAIL_HOST_USER,
            ("nicat254memmedov@gmail.com",),
            fail_silently=False,
            )
                send_mail(
            'Qeydiyyat ucun tesekkurler',
            f"Sizinle tezlikle elaqe saxlanilacaq ! Hormetle Onecast agency",
            settings.EMAIL_HOST_USER,
            (user.email,),
            fail_silently=False,
            )
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

        userdata = {'username':data.pop('username'),
                    'email':data.pop('email'),
                    'password':data.pop('password')}

        user_serializer = UserRegisterSerializer(data=userdata)
        
        if user_serializer.is_valid():

            user = user_serializer.save()
        else:
            print(user_serializer.errors)
            return Response(status=400)
       
        data['user'] = user.id
        profile_serializer = CompanySerializer(data = data)
        print('222')
        profile_serializer.is_valid(raise_exception=True)
        profile_serializer.save()
        
        return Response({"Status": "success"}, status=200)
#homepage 
class HomePageTalentsView(generics.ListAPIView):
    serializer_class = ProfileForHomaPageTalentSerializer
    
    def get_queryset(self):
        queryset = Profile.objects.filter(is_premium = True,is_active=True)[0:12]
        if queryset.count()<12:
            count = 12-queryset.count()
            queryset2 = Profile.objects.filter(is_active = True, is_premium=True).order_by('-created_at')
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


class CompanyPageView(APIView):

    def get(self,request):
        
        queryset = Company.objects.get(user = self.request.user.id)
        serializer = CompanyForSingleSerializer
        employee = serializer(queryset)
        return Response(employee.data)    

    
class TalentModelFilterPage(generics.ListAPIView):
    serializer_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = Custom9Pagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_model=True)

class TalentChildFilterPage(generics.ListAPIView):
    serializer_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = Custom9Pagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_child=True)

class TalentActorFilterPage(generics.ListAPIView):
    serializer_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = Custom9Pagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_actor=True)
    
class TalentAllFilterPage(generics.ListAPIView):
    serializer_class = ProfileForFilterPageSerializer
    pagination_class = Custom12Pagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True,is_premium=True)

class TalentFilterPage(generics.ListAPIView):
    serializer_class = ProfileForFilterPageSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = ProductFilter
    pagination_class = Custom9Pagination
    
    def get_queryset(self):
        return Profile.objects.filter(is_active=True).order_by('-is_premium')
    
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
        if not obj.check_password(serializer.validated_data['expassword']):
                return Response({"error": "Parol doğru değil."}, status=400)
        serializer.save()
        return Response({'Status':'Success'}, status=201)
    
class AboutMeEditView(APIView):
    queryset = About_me.objects.all()
    
    def put(self,request,*args,**kwargs):
        data = self.request.data
        instance = About_me.objects.get(id = data.pop("id"))
        languages = []
        for key, value in data.pop('languages').items():
            if value:
                item = Languages.objects.get(name=key)
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
    lookup_field = 'id'
    
    def perform_update(self, serializer):
        # Call the superclass's perform_update method
        super().perform_update(serializer)

        # Get the updated profile object
        profile = serializer.instance
        email = EmailMessage(
            'Login edildi',
            'Here is the message content. You can include additional text.',
            settings.EMAIL_HOST_USER,
            ["nicat254memmedov@gmail.com"],
        )
   
        email.attach_file(serializer.instance.image1.path)
        email.attach_file(serializer.instance.image2.path)
        email.attach_file(serializer.instance.image3.path)

        email.send(fail_silently=False)    

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
    
class GetActiveOrNot(APIView):
    def put(self,request,*args,**kwargs):
        data = self.request.data
        id = data.get("id")
        profile = Profile.objects.get(id=id)
        profile.is_active = data.get("is_active")
        profile.save()
        return Response({"message":"success"},status=200)
    
class GetVisibleOrNot(APIView):
    def put(self,request,*args,**kwargs):
        data = self.request.data
        id = data.get("id")
        profile = Profile.objects.get(id= id)
        profile.is_visible = data.get("is_visible")
        profile.save()
        return Response({"message":"success"},status=200)
    
class ActorCategoryList(generics.ListAPIView):
    queryset = ActorCategory.objects.all()
    serializer_class = ActorCategoryListSerializer
    
class ModelCategoryList(generics.ListAPIView):
    queryset = ModelCategory.objects.all()
    serializer_class = ModelCategoryListSerializer
    
    
class CompanySettingsEditView(APIView):
    def put(self,request):
        # user = self.request.user
        data=request.data
        number = data.pop('phone_number')
        first_name = data.pop('first_name')
        last_name = data.pop('last_name')
        profile_id = data.pop('profile_id')
        instance = Company.objects.get(id = profile_id)
        pserializer = CompanySerializerForSettingEdit(instance,data = {'phone_number':number,'first_name':first_name,'last_name':last_name},partial=True)
        pserializer.is_valid(raise_exception=True)
        pserializer.save()     
        userinstance = request.user
        userseria = UserSerializerForSettingEdit(userinstance,data=data,partial=True)
        userseria.is_valid()
        userseria.save()

        return Response({'message':'success'},status=200)
    
class CompanyCategoryEditView(APIView):
    queryset = Profile.objects.all()
    
    def put(self,request,*args,**kwargs):
        data2 = self.request.data
        data = data2.pop('categories')
        instance = Company.objects.get(id = data2.pop("id"))
        items = ProductionCategory.objects.filter(name__in=data)
        instance.category.set(items)
        instance.save()
        serializer = CompanySerializerForEdit(instance,data2,partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({"message":"success"},status=200)
    
class EditCompanyImageView(generics.UpdateAPIView):
    queryset = Company.objects.all()
    serializer_class = CompanyImageSerializer
    lookup_field = 'id'

class FilteredModelsView(APIView):
    def get(self, request):
        title = request.GET.get('title')  
        
        name_parts = title.split(" ")
        query = Q()
        
        if len(name_parts) == 1:
            query = Q(first_name__icontains=title) | Q(last_name__icontains=title)
        if len(name_parts)>1:
            query = Q(last_name__icontains=name_parts[1]) & Q(first_name__icontains=name_parts[0])
            query |= Q(last_name__icontains=name_parts[0]) & Q(first_name__icontains=name_parts[1])
        model1_objects = Profile.objects.filter(query)
     
        model2_objects = Company.objects.filter(company_name__icontains=title)
        modelsobj = model1_objects.filter(is_model=True)
        actorsobj = model1_objects.filter(is_actor=True)
        childsobj = model1_objects.filter(is_child=True)
        models = FilterProfileSerializer(modelsobj, many=True)
        actors = FilterProfileSerializer(actorsobj, many=True)
        childs = FilterProfileSerializer(childsobj, many=True)
        serialized_model2 = FilterCompanySerializer(model2_objects, many=True)
        
        return Response({
            'model': models.data,
            'actors': actors.data,
            'childs': childs.data,
            'company': serialized_model2.data
        })