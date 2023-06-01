from django.urls import path
from castingapp.views import *

app_name = "onecast"

urlpatterns = [
    path('HomePageMagazineView/',HomePageMagazineView.as_view(), name='HomePageMagazineView'),
    path('HomePagePartnersView/',HomePagePartnersView.as_view(), name='HomePagePartnersView'),
    path('AddFavView/',AddFavView.as_view(), name='AddFavView'),
    path('ListFavView/',ListFavView.as_view(), name='ListFavView'),
    path('DeleteFromFav/<int:id>',DeleteFromFav.as_view(), name='DeleteFromFav'),
    path('AddSentedView/',AddSentedView.as_view(), name='AddSentedView'),
    path('DeleteFromCard/<int:id>',DeleteFromCard.as_view(), name='DeleteFromCard'),
    path('MagazinListView/',MagazinListView.as_view(), name='MagazinListView'),
    path('MagazinListViewDesc/',MagazinListViewDesc.as_view(), name='MagazinListView'),
    path('MagazineSingleView/<slug>',MagazineSingleView.as_view(), name='MagazineSingleView'),
    path('ContactView/',ContactView.as_view(), name='ContactView'),
    path('NotificationListView/',NotificationListView.as_view(), name='NotificationListView'),
    path('SentedListView/',SentedListView.as_view(), name='SentedListView'),
    path('OneNewsView/<slug>',OneNewsView.as_view(), name='OneNewsView'),
    path('OneNewsCover/',OneNewsCover.as_view(), name='OneNewsCover'),
    path('OneNewsView/',OneNewsView.as_view(), name='OneNewsView'),
    path('NotificationForChild/',NotificationForChild.as_view(), name='NotificationForChild'),
    path('NotificationForCompany/',NotificationForCompany.as_view(), name='NotificationForCompany'),
    path('NotificationForActor/',NotificationForActor.as_view(), name='NotificationForActor'),
    path('NotificationForModel/',NotificationForModel.as_view(), name='NotificationForModel'),
]






