# encoding: utf-8

from django.http import HttpResponse
from ads.models import Unit, Ad, AdMainPic
import json
import logging
import datetime
import hashlib
import logging

log_filename = 'ads_click.log'
log_format = '%(filename)s [%(asctime)s] [%(levelname)s] %(message)s'
logging.basicConfig(format = log_format,
                    filename=log_filename,
                    datefmt='%Y-%m-%d %H:%M:%S',
                    level=logging.DEBUG
)

def index(request):
    return HttpResponse("hello, tino!")

def get_ads(request):
    response_data = {}
    response_data['status'] = {}
    response_data['status']['code'] = 0
    response_data['status']['description'] = u'广告获取成功'
    response_data['info'] = {}
    response_data['info']['units'] = []

    global_image = AdMainPic.objects.filter(id=1)
    if len(global_image) > 0:
        response_data['info']['image'] = global_image[0].pic
    else:
        response_data['info']['image'] = ''



    for unit_obj in Unit.objects.all():
        unit = {}
        unit['unit_title'] = unit_obj.unit_title
        unit['unit_id'] = unit_obj.unit_id
        unit['unit_image'] = unit_obj.unit_image
        unit['unit_type'] = unit_obj.unit_type

        ads = []
        for ad_obj in unit_obj.ad_set.all():
            ad = {}
            ad['id'] = hashlib.md5(str(ad_obj.id+1)).hexdigest()
            ad['title'] = ad_obj.app_name
            ad['image'] = ad_obj.app_image
            ad['description'] = ad_obj.app_description
            ad['url'] = ad_obj.app_url
            ad['store_id'] = ad_obj.app_store_id
            ad['image'] = ad_obj.app_image
            ad['count'] = ad_obj.app_count
            ad['type'] = ad_obj.app_type
            ad['level'] = ad_obj.app_level
            ads.append(ad)
        unit['ads'] = ads

        response_data['info']['units'].append(unit)

    return HttpResponse(json.dumps(response_data), content_type="application/json");

def click(request):
    response_data = {}
    response_data['status'] = {}
    response_data['info'] = {}

    post = request.body
    print 'json_dumps:', json.dumps(post, indent=2)
    try:
        info = json.loads(post)
        app_id = info['app_id']
        app_version = info['app_version']
        user_id = info['user_id']
        ad_id = info['ad_id']
        logging.info('Click:%s\001%s\001%s\001%s' % (app_id, app_version, user_id, ad_id))
    except:
        response_data['status']['code'] = 1
        response_data['status']['description'] = u'输入错误'
        return HttpResponse(json.dumps(response_data), content_type="application/json");

    response_data['status']['code'] = 0
    response_data['status']['description'] = u'记录成功'
    return HttpResponse(json.dumps(response_data), content_type="application/json");
