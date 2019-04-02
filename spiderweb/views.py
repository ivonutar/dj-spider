from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect



import requests
from bs4 import BeautifulSoup

from .models import Target
from .forms import TargetForm

# Create your views here.


def index(request):

    targets_list = Target.objects.all()
    return HttpResponse(targets_list)


def target(request):
    if request.method == 'POST':
        form = TargetForm(request.POST)
        if form.is_valid():
            Target(url=form.data.get('url')).save()
            # TODO not correct
            return HttpResponseRedirect('/')
        else:
            return HttpResponseRedirect('/')
    else:
        form = TargetForm()
    return render(request, 'target.html', {'form': form})


def links(request):

    if request.method == 'POST':
        form = TargetForm(request.POST)
        target_url = form.data.get('url')
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
        return HttpResponse('<br>'.join(links))

    else:
        form = TargetForm()
        return render(request, 'target.html', {'form': form})