from rest_framework import viewsets
from .models import Target
from . serializers import TargetSerializer
import requests
from bs4 import BeautifulSoup
from django.http import HttpResponse
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
        try:
            r = requests.get('{}'.format(target_url))
        except requests.exceptions.MissingSchema as ex:
            return HttpResponse("Error: {}".format(ex))
        html = r.text
        soup = BeautifulSoup(html)
        links = list()
        for link in soup.find_all('a'):
            link_url = link.get('href')
            if link_url in ['#']:
                pass
            else:
                links.append(link_url)
        links = sorted(links)
        return Response({'paths': links})
