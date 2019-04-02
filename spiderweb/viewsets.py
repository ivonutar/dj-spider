from rest_framework import viewsets
from .models import Target
from . serializers import TargetSerializer
from .utils import get_links
from rest_framework.decorators import action
from rest_framework.response import Response


class TargetViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    @action(detail=True, methods=['post'])
    def spider(self, request, **kwargs):

        target_id = kwargs.get('pk')
        target_url = Target.objects.get(id=target_id).target_url

        links = list()
        links.append(get_links(target_url))

        return Response({'paths': links})
