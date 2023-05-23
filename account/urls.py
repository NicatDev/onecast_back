from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from account.views import GetVisibleOrNot,GetActiveOrNot,ModelCategoryList,ActorCategoryList,GetPremiumOrBasic,CategoryEditView,ProfileImageEdit,AboutMeEditView,ChangePasswordVerifyView,TalentSettingEditView,CheckUsername,CompanyListView,TalentFilterPage,TalentAllFilterPage,TalentActorFilterPage,TalentChildFilterPage,TalentModelFilterPage,TalentPageView,CompanyLoginView,TalentLoginView,RegistrationView,CompanyRegisterView,HomePagePopularView,HomePageTalentsView,TalentSingleView

from rest_framework_simplejwt import views as jwt_views
app_name = "accounts-api"

urlpatterns = [
    #auth
    path("login/talent/", TalentLoginView.as_view(), name="login"),
    path("login/company/", CompanyLoginView.as_view(), name="login"),
    path('api/token/',jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('talentRegister/',RegistrationView.as_view(), name='tlntrg'),
    path('companyRegister/',CompanyRegisterView.as_view(), name='cmpnyrg'),
    path('CheckUsername/',CheckUsername.as_view(), name='CheckUsername'),
    #homepage
    path('HomePagePopularView/',HomePagePopularView.as_view(), name='HomePagePopularView'),
    path('HomePageTalentsView/',HomePageTalentsView.as_view(), name='HomePageTalentsView'),
    #singlepage
    path('TalentSingleView/<int:id>',TalentSingleView.as_view(), name='TalentSingleView'),
    path('TalentPageView/',TalentPageView.as_view(), name='TalentPageView'),
    #talentcompanypage
    path('TalentModelFilterPage/',TalentModelFilterPage.as_view(), name='TalentModelFilterPage'),
    path('TalentActorFilterPage/',TalentActorFilterPage.as_view(), name='TalentActorFilterPage'),
    path('TalentChildFilterPage/',TalentChildFilterPage.as_view(), name='TalentChildFilterPage'),
    path('TalentAllFilterPage/',TalentAllFilterPage.as_view(), name='TalentAllFilterPage'),
    path('TalentFilterPage/',TalentFilterPage.as_view(), name='TalentFilterPage'),
    path('CompanyListView/',CompanyListView.as_view(), name='CompanyListView'),
      
    path('TalentSettingEditView/',TalentSettingEditView.as_view(), name='TalentSettingEditView'),  
    path('ChangePasswordVerifyView/<int:id>',ChangePasswordVerifyView.as_view(), name='ChangePasswordVerifyView'),  
    path('AboutMeEditView/',AboutMeEditView.as_view(), name='AboutMeEditView'),  
    path('AboutMeEditView/<int:id>',AboutMeEditView.as_view(), name='AboutMeEditView'),  
    path('ProfileImageEdit/<int:id>',ProfileImageEdit.as_view(), name='ProfileImageEdit'),  
    path('CategoryEditView/',CategoryEditView.as_view(), name='CategoryEditView'),  
    path('GetPremiumOrBasic/',GetPremiumOrBasic.as_view(), name='GetPremiumOrBasic'),  
    path('ActorCategoryList/',ActorCategoryList.as_view(), name='ActorCategoryList'),  
    path('ModelCategoryList/',ModelCategoryList.as_view(), name='ModelCategoryList'),  
    path('GetActiveOrNot/',GetActiveOrNot.as_view(), name='GetActiveOrNot'),  
    path('GetVisibleOrNot/',GetVisibleOrNot.as_view(), name='GetVisibleOrNot'),  
] 



