from django.contrib import admin
from django.urls import path, include
from . import views
from users.views import CustomAuthToken
from django.http import HttpResponse
from django.views.generic.base import RedirectView

urlpatterns = [
    path('fundraisers/', views.FundraiserListView.as_view()),
    path('fundraisers/<int:pk>/', views.FundraiserDetail.as_view()),
    path('fundraisers/<int:pk>/children/', views.ChildrenTotal.as_view()), 
    ## int:pk means we will get a unique integer ID for each fundraiser
    path('pledges/', views.PledgeList.as_view()),
    ## Maybe all this will fix Heroku
    path("", RedirectView.as_view(url="/fundraisers/", permanent=False)),  # <- add this
    path("admin/", admin.site.urls),
    path('', include('fundraisers.urls')),
    path('', include('children.urls')),
    path('', include('users.urls')),
    path('api-token-auth/', CustomAuthToken.as_view(), name='api_token_auth'),
]