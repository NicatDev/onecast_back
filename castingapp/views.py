from django.shortcuts import render
from urllib import request
from rest_framework.decorators import api_view
from rest_framework import generics
from rest_framework import status
from rest_framework.response import Response
from castingapp.models import *
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.pagination import LimitOffsetPagination
from castingapp.paginations import *
from .serializers import *
from .filters import MagazineFilter,NotificationFilter
from rest_framework.views import APIView
from rest_framework.mixins import RetrieveModelMixin
from rest_framework.permissions import BasePermission, IsAuthenticated, SAFE_METHODS

#Homepage
class HomePageMagazineView(generics.ListAPIView):
    serializer_class = MagazineSerializer
    
    def get_queryset(self):
        queryset = News.objects.all().order_by('-created_at')[0:3]
        return queryset

class HomePagePartnersView(generics.ListAPIView):
    serializer_class = PartnersSerializer
    queryset = Partners.objects.all()
 
#END Homepage 
    
#Fav
class AddFavView(generics.CreateAPIView):
    # permission_classes = [IsAuthenticated]
    serializer_class = FavouritesAddSerializer
    queryset = Favourites.objects.all()

        
    def perform_create(self, serializer):
        
        talent = serializer.validated_data.get('talent')
        
        if Favourites.objects.filter(user=self.request.user, talent=talent).exists():
  
            raise serializers.ValidationError("Favourite already exists for this user and talent")
        return serializer.save(user=self.request.user)
    
class ListFavView(generics.ListAPIView):
    serializer_class = FavouritesListSerializer
    
    def get_queryset(self):
        user = self.request.user
        queryset = Favourites.objects.filter(user = user)
        return queryset
    
class DeleteFromFav(generics.DestroyAPIView):
    queryset = Favourites.objects.all()
    serializer_class = FavouritesDeleteSerializer
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.delete()

class DeleteFromFavWithTalentId(APIView):
    def post(self,request):
        talent_id = self.request.data.get('talent_id')
        user = self.request.user
        print(user)
        
        try:
            fav = Favourites.objects.get(user=user,talent=talent_id)
        except:
            fav = '1'
        if fav != '1':
            fav.delete()
        else:
            return Response({"message":"Not exists"},status=200)

        return Response({"message":"Sucess"},status=204)
#End Fav
# class SentCard(models.Model):
#     user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='cards')
#     accepted = models.BooleanField(default=False)
#     desitiondate = models.DateField(auto_now_add=True)
    
#     def __str__(self):
#         return f'{self.user.username}-{self.accepted}-{self.desitiondate}'
    
# class CardItem(models.Model):
#     card = models.ForeignKey(SentCard,on_delete=models.CASCADE,related_name='items')
#     talent = models.ForeignKey(Profile,on_delete=models.CASCADE)

#sentbyyou
from rest_framework.views import APIView
class AddSentedView(APIView):

    def post(self,request):
        print('2')
        user = self.request.user
        data = self.request.data
        print('1')
        
        if not SentCard.objects.filter(user=user).exists():
            cardserializer = SentCardSerializer(data={'user':user.id})
            cardserializer.is_valid(raise_exception=True)
            card = cardserializer.save()
        else:
            card = SentCard.objects.get(user=user.id)
        print('2')
        data['card'] = card.id
        
        talent = data.get('talent')
        if CardItem.objects.filter(card__user=self.request.user, talent=talent).exists():
            return Response({"Already exists"},status=400)
            
        carditemserializer = CardItemSerializer(data=data)
        carditemserializer.is_valid(raise_exception=True)
        carditemserializer.save()
        
        return Response({"message":'success'},status=201)

#url with id
class DeleteFromCard(generics.DestroyAPIView):
    queryset = CardItem.objects.all()
    serializer_class = CardItemSerializer
    lookup_field = 'id'

    def perform_destroy(self, instance):
        instance.delete()
        
class SentedListView(generics.ListAPIView):
    serializer_class = CardItemForSentedSerializer
    def get_queryset(self):
        return CardItem.objects.filter(card__user = self.request.user)
        
#Magazinepage
class MagazinListView(generics.ListAPIView):
    serializer_class = MagazineSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MagazineFilter
    
    def get_queryset(self):
        return News.objects.all().order_by('-created_at')
    
class MagazinListViewDesc(generics.ListAPIView):
    serializer_class = MagazineSerializer
    filter_backends = (DjangoFilterBackend,)
    filterset_class = MagazineFilter
    
    def get_queryset(self):
        return News.objects.all().order_by('created_at')
    
class NotificationListView(generics.ListAPIView):
    serializer_class = MagazineSerializer
    
    def get_queryset(self):
        return News.objects.all().order_by('-created_at')[0:10]
    
class MagazineSingleView(generics.RetrieveAPIView):
    serializer_class = MagazineSerializer
    queryset = News.objects.all()
    lookup_field = 'slug'
    
    
class ContactView(generics.CreateAPIView):
    serializer_class = ContactUsSerializer
    queryset = Contact_us.objects.all()
    
class NotificationView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    queryset = Notification.objects.all()

    
    def get_queryset(self):
        queryset = []
        user = self.request.user
        print('baslangic')
        if user.is_authenticated:

            com = Company.objects.filter(user=user).exists()
            tal = Profile.objects.filter(user=user).exists()
            print(com,tal)
            if com:
            
                queryset = Notification.objects.filter(company=Company.objects.get(user=user)) | Notification.objects.filter(for_company = True)[0:10]
            elif tal:
             
                talent = Profile.objects.get(user=user)
                if talent.is_child == True:
                    queryset = Notification.objects.filter(talant=talent) | Notification.objects.filter(for_child = True)[0:10]
                elif talent.is_model==True: 
                    queryset = Notification.objects.filter(talant=talent) | Notification.objects.filter(for_model = True)[0:10]
                elif talent.is_actor==True:
                    queryset = Notification.objects.filter(talant=talent) | Notification.objects.filter(for_actor = True)[0:10]
            else:
                queryset = Notification.objects.filter(for_none_users = True)[0:10]
        return queryset
    

    
class OneNewsView(generics.ListAPIView):
    pagination_class = Custom6Pagination
    serializer_class = OneNewsSerializer
    queryset = OneNews.objects.all()
    
class OneNewsCover(generics.ListAPIView):
    serializer_class = OneNewsCoverSerializer
    
    def get_queryset(self):
        return OneNewsCover.objects.all()[0:3]
    
class OneNewsSingleView(generics.RetrieveAPIView):
    serializer_class = OneNewsSerializer
    queryset = OneNews.objects.all()
    lookup_field = 'slug'
        
class ConfirmView(APIView):
    def post(self,request):
        cards = CardItem.objects.filter(card__user = self.request.user)
        company = Company.objects.get(user = self.request.user)
        talents = ''
        for x in cards:
            talents = talents + x.talent.first_name + ' ' + x.talent.last_name + ',' + ' '
        confirm = ConfirmSerializer(data = {'company':company.id,'talents':talents})
        confirm.is_valid(raise_exception=True)
        confirm.save()
        return Response(status=201)
        
class HomePageImageView(generics.ListAPIView):
    serializer_class = HomePageImageSerializer
    queryset = HomePageImage.objects.all()
            
        