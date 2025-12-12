from django.urls import path
from . import views

urlpatterns = [
    path('fundraisers/', views.FundraiserListView.as_view()),
    path('fundraisers/<int:pk>/', views.FundraiserDetail.as_view()),
    path('fundraisers/<int:pk>/children/', views.ChildrenTotal.as_view()), 
    ## int:pk means we will get a unique integer ID for each fundraiser
    path('pledges/', views.PledgeList.as_view()),
]