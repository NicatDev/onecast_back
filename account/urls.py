from django.urls import path
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from account.views import TalentActorFilterPage,TalentChildFilterPage,TalentModelFilterPage,TalentPageView,LoginView,RegistrationView,CompanyRegisterView,HomePagePopularView,HomePageTalentsView,TalentSingleView

from rest_framework_simplejwt import views as jwt_views
app_name = "accounts-api"

urlpatterns = [
    path("login/", LoginView.as_view(), name="login"),
    path('api/token/',jwt_views.TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/',jwt_views.TokenRefreshView.as_view(), name='token_refresh'),
    path('talentRegister/',RegistrationView.as_view(), name='tlntrg'),
    path('companyRegister/',CompanyRegisterView.as_view(), name='cmpnyrg'),
    path('HomePagePopularView/',HomePagePopularView.as_view(), name='HomePagePopularView'),
    path('HomePageTalentsView/',HomePageTalentsView.as_view(), name='HomePageTalentsView'),
    path('TalentSingleView/<int:id>',TalentSingleView.as_view(), name='TalentSingleView'),
    path('TalentPageView/',TalentPageView.as_view(), name='TalentPageView'),
    path('TalentModelFilterPage/',TalentModelFilterPage.as_view(), name='TalentModelFilterPage'),
    path('TalentActorFilterPage/',TalentActorFilterPage.as_view(), name='TalentActorFilterPage'),
    path('TalentChildFilterPage/',TalentChildFilterPage.as_view(), name='TalentChildFilterPage'),
    
]


