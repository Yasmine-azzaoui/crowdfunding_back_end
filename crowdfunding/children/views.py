from django.shortcuts import render

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from .permissions import IsOwnerOrReadOnly
from django.http import Http404
from .models import Children
from .serializers import ChildrenSerializer
from fundraisers.models import Fundraiser


class ChildrenListView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        children = Children.objects.all()
        serializer = ChildrenSerializer(children, many=True)
        return Response(serializer.data)
    
    def post(self, request):
        fundraiser_id = (
            request.data.get('fundraisers')
            or request.data.get('fundraiser')
            or request.data.get('fundraiser_id')
        )
        if not fundraiser_id:
            return Response({'detail': 'fundraiser id is required'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            fundraiser = Fundraiser.objects.get(pk=fundraiser_id)
        except Fundraiser.DoesNotExist:
            return Response({'detail': 'fundraiser not found'}, status=status.HTTP_404_NOT_FOUND)

        owner = getattr(fundraiser, 'owner', None) or getattr(fundraiser, 'user', None) or getattr(fundraiser, 'creator', None)
        if owner != request.user:
            return Response({'detail': 'Only the fundraiser owner can add children'}, status=status.HTTP_403_FORBIDDEN)

        serializer = ChildrenSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(fundraisers=fundraiser)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ChildrenDetail(APIView):
    def get_object(self, pk):
        try:
            children = Children.objects.get(pk=pk)
            self.check_object_permissions(self.request, children)
            return children
        except Children.DoesNotExist:
            raise Http404

    def get(self, request, pk):
        children = self.get_object(pk)
        serializer = ChildrenSerializer(children)
        return Response(serializer.data)

# class PledgeList(APIView):
#     permission_classes = [permissions.IsAuthenticatedOrReadOnly]

#     def get(self, request):
#         pledges = Pledge.objects.all()
#         serializer = PledgeSerializer(pledges, many=True)
#         return Response(serializer.data)

#     def post(self, request):
#         serializer = PledgeSerializer(data=request.data)
#         if serializer.is_valid():
#             serializer.save(owner=request.user)
#             return Response(
#                 serializer.data,
#                 status=status.HTTP_201_CREATED
#             )
#         return Response(
#             serializer.errors,
#             status=status.HTTP_400_BAD_REQUEST
#         )   
