from rest_framework import serializers
from castingapp.models import ConfirmHistory,OneNewsCover,OneNews,News,Partners,Favourites,SentCard,CardItem,Contact_us,Notification
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

    
    class Meta:
        model = CardItem
        fields = '__all__'
        
class CardItemForSentedSerializer(serializers.ModelSerializer):
    talent = ProfileSerializer()
    class Meta:
        model = CardItem
        fields = '__all__'
        
#ContactUs


class ContactUsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Contact_us
        fields = '__all__'
        
class NotificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Notification
        fields = '__all__'
        
class OneNewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneNews
        fields = '__all__'
 
class OneNewsCoverSerializer(serializers.ModelSerializer):
    class Meta:
        model = OneNewsCover
        fields = '__all__'       

class ConfirmSerializer(serializers.ModelSerializer):
    class Meta:
        model = ConfirmHistory
        fields = '__all__'