
from rest_framework import serializers
from django.contrib.auth import get_user_model, authenticate
from django.core.mail import send_mail
from django.conf import settings

from account.models import *

User = get_user_model()
class AboutMeForRegisterSerializer(serializers.ModelSerializer):
    class Meta:
        model = About_me
        exclude = ('language',)
        
class UserRegisterSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ("email","password","username", "id")

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        username = attrs.get("username")
        username_qs = User.objects.filter(username=username).exists()
        email_qs = User.objects.filter(email=email).exists()

        if email_qs:
            raise serializers.ValidationError("Bu email ile artiq qeydiyyatdan kecilib")
        if username_qs:
            raise serializers.ValidationError("Bu username ile artiq qeydiyyatdan kecilib")
        if password:
            if len(password) < 6:
                raise serializers.ValidationError("Sifre en azi 6 simvoldan ibaret olmalidir")

        return attrs

    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User(
            **validated_data
        )
        user.set_password(password)
        
        user.is_active = False
        user.save()   

        return user
    
class ProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = '__all__'
        
class CompanySerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        

class ProfileForHomaPageTalentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('id','image1','is_premium','gender','first_name','last_name','is_actor','is_model','is_child',)

class PopularSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Popular
        fields = '__all__'
        
#singleviewserializers

        
class LanguageSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Languages
        fields = '__all__'
    
    
        
class AboutMeSerializer(serializers.ModelSerializer):
    language = LanguageSerializer(many=True)
    languages = serializers.SerializerMethodField()
    class Meta:
        model = About_me
        fields = '__all__'
        
    def get_languages(self,obj):
        languages =  obj.languages.all()
        allang = Languages.objects.all()
        names = []  
        data = {}
        for x in languages:
            names.append(y.name)
        for y in allang:
            if y.name not in names:
                data[y.name] = False
            else:
                data[y.name] = True
        return data
    
class ModelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCategory
        fields = '__all__'
        
class ActorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActorCategory
        fields = '__all__'
        
class UserSerializerUserPage(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = '__all__'
    
class ProfileForSingleSerializer(serializers.ModelSerializer):
    user = UserSerializerUserPage()
    actorCategory = ActorCategorySerializer(many=True)
    modelCategory = ModelCategorySerializer(many=True)
    about_me = AboutMeSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
        
class ProfileForFilterPageSerializer(serializers.ModelSerializer):
 
    class Meta:
        model = Profile
        fields = ('image1','first_name','last_name','is_actor','is_model','is_child','is_premium') 
    
#endofsingleview
class UserSerializerForSettingEdit(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email',)

class ProfileSerializerForSettingEdit(serializers.ModelSerializer):
    class Meta:
        model = Profile
        fields = ('phone_number','first_name','last_name')
        
class CompanyListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Company
        fields = '__all__'
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('password',)
        
class ChangePasswordSerializer(serializers.ModelSerializer):
    password = serializers.CharField(style={"input_type":"password"})

    expassword = serializers.CharField()
    class Meta:
        model = User
        fields = ("expassword", "password")
    def validate(self, attrs):
        
        
        
        expassword = attrs.get("expassword")

        if expassword != self.password:
            raise serializers.ValidationError({"Duzgun kod daxil edilmeyib"})
       
        return attrs

    def update(self,instance,validated_data):
        password = validated_data.pop('password')
        instance.password_reset_code = None
        instance.set_password(password)
        instance.save()
        return instance