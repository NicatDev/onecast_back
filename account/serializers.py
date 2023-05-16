
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
        fields = ('id','image1','is_premium','gender','first_name','last_name','is_actor','is_model','age','height','eyecolor','weight',)

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
    class Meta:
        model = About_me
        fields = '__all__'
        
class ModelCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ModelCategory
        fields = '__all__'
        
class ActorCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = ActorCategory
        fields = '__all__'
    
class ProfileForSingleSerializer(serializers.ModelSerializer):
    actorCategory = ActorCategorySerializer(many=True)
    modelCategory = ModelCategorySerializer(many=True)
    about_me = AboutMeSerializer()

    class Meta:
        model = Profile
        fields = '__all__'
        
#endofsingleview