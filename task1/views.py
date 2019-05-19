from django.shortcuts import render
from django.views.generic import TemplateView
from .models import Station, Net, Networkstations
from django.http import HttpResponse
from django.core.serializers.json import DjangoJSONEncoder
import json


def filter(request):
    if request.GET:
        filter = request.GET.get('filter')
        decoded_filter = json.loads(filter)  # из строки инициализирует объект
        stations = Station.objects.all()
        id_net = Net.objects.filter(name=decoded_filter["net"])
        list_id_stations = Networkstations.objects.filter(idnet__in=id_net).values_list("idstation", flat=True)
        list_name_net = []
        stations_out = []
        if decoded_filter["net"] != 'all':
            stations = stations.filter(id__in=list_id_stations)
        if decoded_filter["type"] != 'all':
            stations = stations.filter(type=decoded_filter["type"])
        for station in stations:
            stations_out.append(
                {'sitecode': station.sitecode, 'name': station.name, 'latitude': station.latitude,
                 'longitude': station.longitude, 'type': station.type, 'link': station.link, })
        for station in stations:
            list_name_net.append(
                list(Networkstations.objects.filter(idstation=station.id).values_list('idnet__name', flat=True)))
        ctx = {
            'stations': stations_out,
            'list_name_net': list_name_net,
        }

    return HttpResponse(json.dumps(ctx, cls=DjangoJSONEncoder), content_type='application/json')


class List(TemplateView):
    template_name = 'station_list.html'

    def get(self, request):
        stations = Station.objects.all()
        list_name_net = []
        stations_out = []

        for station in stations:
            list_name_net.append(
                list(Networkstations.objects.filter(idstation=station.id).values_list('idnet__name', flat=True)))

        for station in stations:
            stations_out.append(
                {'sitecode': station.sitecode, 'name': station.name, 'latitude': station.latitude,
                 'longitude': station.longitude, 'type': station.type, 'link': station.link, })
        ctx = {
            'stations': json.dumps(stations_out, cls=DjangoJSONEncoder),
            'list_name_net': json.dumps(list_name_net, cls=DjangoJSONEncoder),
        }
        return render(request, self.template_name, ctx)
