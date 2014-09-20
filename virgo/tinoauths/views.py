# encoding: utf-8

from django.shortcuts import render
from django.http import HttpResponse
from tinoauths.models import User
import json
import sys

import hashlib


def index(request):
    return HttpResponse('tino auth')


def active(request):
    response_data = {}
    response_data['status'] = {}
    response_data['info'] = {}

    post = request.body
    print 'json_dumps:', json.dumps(post, indent=2)
    try:
        info = json.loads(post)
        device_info = info['device_info']
        imei = device_info['imei']
        print 'imei: ', imei
        idfa = device_info['idfa']
        print 'idfa: ', idfa
        open_udid = device_info['open_udid']
        print 'open_udid: ', open_udid
    except:
        response_data['status']['code'] = 1
        response_data['status']['description'] = u'输入错误'
        return HttpResponse(json.dumps(response_data), content_type="application/json");



    duplicate_imei_objs = User.objects.filter(imei=imei)
    duplicate_idfa_objs = User.objects.filter(idfa=idfa)
    duplicate_open_udid_objs = User.objects.filter(open_udid=open_udid)

    obj_set = set(duplicate_open_udid_objs) | set(duplicate_idfa_objs) | set(duplicate_open_udid_objs)
    if len(obj_set) > 1:
        response_data['status']['code'] = 2
        response_data['status']['description'] = u'重复的imei/idfa/open_udid'
        return HttpResponse(json.dumps(response_data), content_type="application/json");

    if len(obj_set) == 1:
        user = obj_set.pop()
        # print '1:', user.imei
        # print '1:', user.idfa
        # print '1:', user.open_udid
        try:
            user.imei = imei
            user.idfa = idfa
            user.open_udid = open_udid
            user.save()
        except:
            response_data['status']['code'] = 3
            response_data['status']['description'] = u'新用户激活失败'
            return HttpResponse(json.dumps(response_data), content_type="application/json");

        response_data['status']['code'] = 0
        response_data['status']['description'] = u'用户已经存在'
        response_data['info']['uid'] = user.uid

        return HttpResponse(json.dumps(response_data), content_type="application/json");

    if len(obj_set) == 0:
        uid = hashlib.md5(imei+idfa+open_udid).hexdigest()
        try:
            news_user = User.objects.create(imei=imei, idfa=idfa, open_udid=open_udid, uid=uid)
            # print '1:', news_user.imei
            # print '1:', news_user.idfa
            # print '1:', news_user.open_udid
        except:
            response_data['status']['code'] = 3
            response_data['status']['description'] = u'新用户激活失败'
            return HttpResponse(json.dumps(response_data), content_type="application/json");

        response_data['status']['code'] = 0
        response_data['status']['description'] = u'新用户激活成功'
        response_data['info']['uid'] = news_user.uid
        return HttpResponse(json.dumps(response_data), content_type="application/json");

    return HttpResponse(response_data)
