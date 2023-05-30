from rest_framework import serializers
from castingapp.models import News,Partners,Favourites,SentCard,CardItem,Contact_us
from account.serializers import ProfileSerializer
class MagazineSerializer(serializers.ModelSerializer):
    class Meta:
        model = News
        fields = '__all__'
        
class PartnersSerializer(serializers.ModelSerializer):
    class Meta:
        model = Partners
        fields = '__all__'
        
class FavouritesAddSerializer(serializers.ModelSerializer):
    class Meta:
        model = Favourites
        exclude = ('user',)
        
    def validate(self,attrs):
        user = attrs.get('user')
        talent = attrs.get('talent')
  
        if Favourites.objects.filter(user=user, talent=talent).exists():
            
            raise serializers.ValidationError("Favourite already exists for this user and talent")

        return attrs    
class FavouritesListSerializer(serializers.ModelSerializer):
    talent = ProfileSerializer()
    class Meta:
        model = Favourites
        fields = '__all__'
    
class FavouritesDeleteSerializer(serializers.ModelSerializer):

    class Meta:
        model = Favourites
        fields = '__all__'
        
class SentCardSerializer(serializers.ModelSerializer):
    class Meta:
        model = SentCard
        fields = '__all__'
    
# 1addsentedview 2deletefromcardview
class CardItemSerializer(serializers.ModelSerializer):
    sentcard = SentCardSerializer()
    
    class Meta:
        model = CardItem
        fields = '__all__'
        
#ContactUs


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_us
        fields = '__all__'