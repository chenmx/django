# encoding: utf-8

from django.shortcuts import render, render_to_response
from django.http import HttpResponse, HttpResponseRedirect
from models import MonthlyWeatherByCity
from chartit import DataPool, Chart

def index(request):
    return HttpResponse('123')

def weather_chart_view(request):
#Step 1: Create a DataPool with the data we want to retrieve.
    weatherdata = \
        DataPool(
            series=
                [{'options':
                    {
                        'source': MonthlyWeatherByCity.objects.all()},
                        'terms':
                        [
                            'month',
                            'houston_temp',
                            'boston_temp',
                            'newyork_temp'
                        ]
                    }
        ])

#Step 2: Create the Chart object
    cht = Chart(
        datasource = weatherdata,
        series_options =
            [{'options':{
            'type': 'line',
            'stacking': False},
            'terms':{
            'month': [
            'boston_temp',
            'houston_temp',
            'newyork_temp'
            ]
        }}],
        chart_options =
            {'title': {
            'text': '第一个报表'},
            'xAxis': {
            'title': {
            'text': 'Month number'}}})

#Step 3: Send the chart object to the template.
    # return render_to_response({'weatherchart': cht})
    return render(request, 'charts/weatherchart.html', {'weatherchart': cht})
    # cht = {'Chrome': 52.9, 'Opera': 1.6, 'Firefox': 27.7}
    # context = {'data': cht}
    # return render(request, 'charts/weatherchart.html', context)
