from rest_framework import viewsets
from .models import Target
from . serializers import TargetSerializer


class TargetViewSet(viewsets.ModelViewSet):
    http_method_names = ['GET', 'POST']
    queryset = Target.objects.all()
    serializer_class = TargetSerializer
