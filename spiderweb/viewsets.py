from rest_framework import viewsets
from .models import Target
from . serializers import TargetSerializer
from .utils import spider
from rest_framework.decorators import action
from rest_framework.response import Response


class TargetViewSet(viewsets.ModelViewSet):
    http_method_names = ['get', 'post']
    queryset = Target.objects.all()
    serializer_class = TargetSerializer

    @action(detail=True, methods=['post'])
    def spider(self, request, **kwargs):

        target_id = kwargs.get('pk')
        target_obj = Target.objects.get(id=target_id)
        starting_point_url = target_obj.starting_point_url
        scope = target_obj.scope

        links = list()
        links.append(spider(starting_point_url, scope))

        return Response({'paths': links})
