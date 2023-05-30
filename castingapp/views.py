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
from .filters import MagazineFilter

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


    def perform_destroy(self, instance):
        instance.delete()
    
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
class AddSentedView(generics.CreateAPIView):
    permission_classes = [IsAuthenticated]
    def post(self):
        user = self.request.user
        data = self.request.data
        if not SentCard.objects.filter(user=user.id).exists():
            cardserializer = SentCardSerializer({'user':user.id})
            cardserializer.is_valid(raise_exception=True)
            card = cardserializer.save()
        else:
            card = SentCard.objects.get(user=user.id)
        data['card'] = card.id
        carditemserializer = CardItemSerializer(data=data)
        carditemserializer.is_valid(raise_exception=True)
        carditemserializer.save()
        return Response({"message":'success'},status=201)

#url with id
class DeleteFromCard(generics.DestroyAPIView):
    queryset = CardItem.objects.all()
    serializer_class = CardItemSerializer


    def perform_destroy(self, instance):
        instance.delete()
        
class SentedListView(generics.ListAPIView):
    serializer_class = CardItemSerializer
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