from django.urls import path
from . import views

urlpatterns = [
    path('children/', views.ChildrenListView.as_view()),
    path('children/<int:pk>/', views.ChildrenDetail.as_view()),
    ## int:pk means we will get a unique integer ID for each children
    # path('pledges/', views.PledgeList.as_view()),
]