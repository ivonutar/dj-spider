from rest_framework import serializers
from .models import Target


class TargetSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Target
        fields = ('url', 'starting_point_url', 'scope')

