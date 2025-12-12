from rest_framework import serializers
from django.apps import apps
from .models import Children
from fundraisers.models import Fundraiser

class ChildrenSerializer(serializers.ModelSerializer):
    fundraiser = serializers.ReadOnlyField(source='fundraiser.id')

    class Meta:
        model = Children
        fields = '__all__'

class ChildrenDetailSerializer(ChildrenSerializer):

    def update(self, instance, validated_data):
        instance.firstname = validated_data.get('firstname', instance.firstname)
        instance.lastname = validated_data.get('lastname', instance.lastname)
        instance.DOB = validated_data.get('DOB', instance.DOB)
        instance.description = validated_data.get('description', instance.description)
        instance.SpecialHelp = validated_data.get('SpecialHelp', instance.SpecialHelp)
        instance.Specify = validated_data.get('Specify', instance.Specify)
        instance.image = validated_data.get('image', instance.image)
        instance.is_open = validated_data.get('is_open', instance.is_open)
        instance.date_created = validated_data.get('date_created', instance.date_created)
        instance.fundraiser = Fundraiser.objects.get(validated_data.get('fundraiser', instance.fundraiser))
        instance.save()
        return instance