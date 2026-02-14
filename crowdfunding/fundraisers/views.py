from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied
from .permissions import IsOwnerOrReadOnly
from django.http import Http404
from .models import Fundraiser, Pledge
from .serializers import FundraiserSerializer, FundraiserDetailSerializer, PledgeSerializer
from children.models import Children 
from children.serializers import ChildrenSerializer


class FundraiserListView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get(self, request):
        fundraisers = Fundraiser.objects.all()
        serializer = FundraiserSerializer(fundraisers, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        serializer = FundraiserSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save(owner=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )

class ChildrenTotal(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def get(self, request, pk):
        children = Children.objects.filter(fundraiser__pk=pk)
        serializer = ChildrenSerializer(children, many=True)
        return Response(serializer.data)

class FundraiserDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
    def get_object(self, pk):
        try:
            return Fundraiser.objects.get(pk=pk)
        except Fundraiser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        fundraiser = self.get_object(pk)
        serializer = FundraiserDetailSerializer(fundraiser)
        return Response(serializer.data)

    def patch(self, request, pk):
        fundraiser = self.get_object(pk)
        # Only owner can update
        if fundraiser.owner != request.user:
            raise PermissionDenied("You can only edit your own fundraisers.")
        
        serializer = FundraiserSerializer(fundraiser, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PledgeList(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request):
        pledges = Pledge.objects.all()
        serializer = PledgeSerializer(pledges, many=True)
        return Response(serializer.data)

    def post(self, request):
        serializer = PledgeSerializer(data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PledgeDetail(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_object(self, pk):
        try:
            return Pledge.objects.get(pk=pk)
        except Pledge.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        pledge = self.get_object(pk)
        serializer = PledgeSerializer(pledge)
        return Response(serializer.data)

class UserDashboard(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        # Get fundraisers created by this user
        my_fundraisers = Fundraiser.objects.filter(owner=request.user)
        # Get pledges made by this user
        my_pledges = Pledge.objects.filter(supporter=request.user)
        
        return Response({
            'my_fundraisers': FundraiserSerializer(my_fundraisers, many=True).data,
            'my_pledges': PledgeSerializer(my_pledges, many=True).data
        })