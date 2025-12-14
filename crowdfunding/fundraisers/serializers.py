from rest_framework import serializers
from django.apps import apps

Pledge = apps.get_model('fundraisers.Pledge')
Fundraiser = apps.get_model('fundraisers.Fundraiser')


class PledgeSerializer(serializers.ModelSerializer):
    supporter = serializers.PrimaryKeyRelatedField(read_only=True)
    fundraiser = serializers.PrimaryKeyRelatedField(queryset=Fundraiser.objects.all())

    class Meta:
        model = Pledge
        fields = [
            'id', 'pledge_type', 'amount', 'hours', 'comment',
            'date_created', 'anonymous', 'fundraiser', 'supporter'
        ]
        read_only_fields = ['id', 'date_created', 'supporter']

    def validate(self, data):
        request = self.context.get('request')
        pledge_type = data.get('pledge_type', Pledge.MONEY)
        anonymous = data.get('anonymous', False)

        if not data.get('fundraiser'):
            raise serializers.ValidationError({'fundraiser': 'This field is required.'})

        if pledge_type == Pledge.MONEY and not data.get('amount'):
            raise serializers.ValidationError({'amount': 'Amount is required for money pledges.'})
        if pledge_type == Pledge.TIME and not data.get('hours'):
            raise serializers.ValidationError({'hours': 'Hours is required for time pledges.'})

        if anonymous and pledge_type == Pledge.TIME:
            raise serializers.ValidationError('Anonymous users cannot commit time.')

        if pledge_type == Pledge.TIME:
            user = getattr(request, 'user', None)
            if not (user and user.is_authenticated):
                raise serializers.ValidationError('Authentication required for time pledges.')
            bluecard = getattr(user, 'bluecard', False)
            if not bluecard:
                raise serializers.ValidationError('Only bluecard users can make time pledges.')

        return data

    def create(self, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        if validated_data.get('anonymous'):
            validated_data['supporter'] = None
        else:
            if not (user and user.is_authenticated):
                raise serializers.ValidationError('Authentication required unless pledge is anonymous.')
            validated_data['supporter'] = user

        return super().create(validated_data)

    def update(self, instance, validated_data):
        request = self.context.get('request')
        user = getattr(request, 'user', None)

        pledge_type = validated_data.get('pledge_type', instance.pledge_type)
        anonymous = validated_data.get('anonymous', instance.anonymous)
        amount = validated_data.get('amount', instance.amount)
        hours = validated_data.get('hours', instance.hours)

        if pledge_type == Pledge.MONEY and not amount:
            raise serializers.ValidationError({'amount': 'Amount is required for money pledges.'})
        if pledge_type == Pledge.TIME and not hours:
            raise serializers.ValidationError({'hours': 'Hours is required for time pledges.'})

        if anonymous and pledge_type == Pledge.TIME:
            raise serializers.ValidationError('Anonymous users cannot commit time.')

        if pledge_type == Pledge.TIME:
            if not (user and user.is_authenticated):
                raise serializers.ValidationError('Authentication required for time pledges.')
            bluecard = getattr(user, 'bluecard', False)
            if not bluecard:
                raise serializers.ValidationError('Only bluecard users can make time pledges.')

        if anonymous:
            validated_data['supporter'] = None
        else:
            if not (user and user.is_authenticated):
                raise serializers.ValidationError('Authentication required unless pledge is anonymous.')
            validated_data['supporter'] = user

        return super().update(instance, validated_data)


class FundraiserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Fundraiser
        fields = ['id', 'title', 'description', 'goal', 'is_open']  


class FundraiserDetailSerializer(FundraiserSerializer):
    # safe: PledgeSerializer is already defined above
    pledges = PledgeSerializer(many=True, read_only=True)