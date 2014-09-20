# encoding: utf-8

from django.contrib import admin
from ads.models import Unit, Ad, AdMainPic
from bs4 import BeautifulSoup
import urllib2

class AdInline(admin.StackedInline):
    model = Ad
    extra = 0

class UnitAdmin(admin.ModelAdmin):
    # fields = ['', '']
    inlines = [AdInline]

    list_display = ('description', 'unit_id', 'pub_date')

class AdMainPicAdmin(admin.ModelAdmin):
    list_display = ('id', 'pic')

class AdAdmin(admin.ModelAdmin):

    list_display = ('app_name', 'unit', 'app_description', 'app_image', 'pub_date')

    def save_model(self, request, obj, form, change):
        if not obj.app_image:
            print 'get imge start'
            url = "https://itunes.apple.com/cn/app/boxpop/id{0}".format(obj.app_store_id)
            print url
            req = urllib2.Request(url,
                    headers = {"Referer": "http://www.baidu.com",
                               "User-Agent": "Mozilla/5.0 (Windows NT 5.1) AppleWebKit/534.24 (KHTML, like Gecko) Chrome/11.0.696.68 Safari/534.24"
                               })
            if req:
                html = urllib2.urlopen(url = req, timeout = 20).read()
                soup = BeautifulSoup(html)

                img_soup = soup.find('meta', {'property':'og:image'})
                if img_soup:
                    print img_soup
                    obj.app_image = img_soup['content']

        obj.save()

admin.site.register(AdMainPic, AdMainPicAdmin)
admin.site.register(Unit, UnitAdmin)
admin.site.register(Ad, AdAdmin)
