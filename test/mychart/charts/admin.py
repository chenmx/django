from django.contrib import admin
from charts.models import MonthlyWeatherByCity

# class MonthlyWeatherByCityPageAdmin(admin.ModelAdmin):
#     pass


admin.site.register(MonthlyWeatherByCity)
