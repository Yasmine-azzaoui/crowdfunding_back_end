from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.exceptions import PermissionDenied
from .permissions import IsOwnerOrReadOnly
from django.http import Http404
from .models import Fundraiser, Pledge
from .serializers import FundraiserSerializer
from .serializers import PledgeSerializer
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
            return Response(
                serializer.data, status=status.HTTP_201_CREATED
                )
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
    def get_object(self, pk):
        try:
            fundraiser = Fundraiser.objects.get(pk=pk)
            self.check_object_permissions(self.request, fundraiser)
            return fundraiser
        except Fundraiser.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        fundraiser = self.get_object(pk)
        serializer = FundraiserSerializer(fundraiser)
        return Response(serializer.data)

class PledgeList(APIView):
    permission_classes = [permissions.AllowAny]  # allow anonymous POST for money pledges

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
    
    def _ensure_can_modify(self, instance):
        user = self.request.user
        if instance.supporter is None:
            raise PermissionDenied('Anonymous pledges cannot be modified.')
        if instance.supporter != user and not user.is_staff:
            raise PermissionDenied('You do not have permission to modify this pledge.')

    def patch(self, request, pk):
        instance = self.get_object(pk)
        self._ensure_can_modify(instance)
        serializer = PledgeSerializer(instance, data=request.data, partial=True, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def put(self, request, pk):
        instance = self.get_object(pk)
        self._ensure_can_modify(instance)
        serializer = PledgeSerializer(instance, data=request.data, context={'request': request})
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        instance = self.get_object(pk)
        self._ensure_can_modify(instance)
        instance.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)