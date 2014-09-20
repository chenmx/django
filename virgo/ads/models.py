# encoding: utf-8

import hashlib

from django.db import models
from datetime import time

class AdMainPic(models.Model):
    pic = models.CharField('广告入口图片地址', max_length=300, blank=True)


class Unit(models.Model):
    UNIT_TYPE_CHOICES = (
            (0, '顶端'),
            (1, '其他'),
    )


    unit_title = models.CharField('推广单元名称', max_length=100)
    unit_id = models.PositiveIntegerField('推广单元ID', unique=True)
    unit_image = models.CharField('推广单元图片地址', max_length=300, blank=True)
    unit_type = models.PositiveIntegerField('推广单元类型', choices=UNIT_TYPE_CHOICES)
    pub_date = models.DateTimeField('最后修改', auto_now=True, auto_now_add=True)

    def description(self):
        return self.unit_title
    description.admin_order_field = 'unit_id'
    description.short_description = '推广单元'

    def __unicode__(self):
        return self.description()

class Ad(models.Model):
    unit = models.ForeignKey(Unit)

    # STATUS_CHOICES = (
    #         ('0', '未知'),
    #         ('1', '未开赛'),
    #         ('2', '已结束'),
    #         ('3', '进行中'),
    # )

    # TIME_CHOICES = (
    #         (time(0,0,0,0), '00:00'),
    #         (time(3,0,0,0), '03:00'),
    #         (time(4,0,0,0), '04:00'),
    #         (time(6,0,0,0), '06:00'),
    #         (time(9,0,0,0), '09:00'),
    # )

    # IMPORTANT_CHOICES = (
    #         ('0', '普通'),
    #         ('1', '重要'),
    #         ('2', '非常重要'),
    # )


    app_name = models.CharField('app名称', max_length = 100)
    app_image = models.CharField('app图片地址', max_length = 300, blank=True)
    app_description = models.TextField('app描述', blank=True)
    app_url = models.CharField('app下载地址', max_length = 300)
    app_store_id = models.CharField('app官方ID', max_length = 300)
    app_count = models.PositiveIntegerField('app下载量')
    app_type = models.CharField('app类型', max_length = 50)
    app_level = models.PositiveIntegerField('app星级')

    pub_date = models.DateTimeField('最后修改', auto_now=True, auto_now_add=True)

    def description(self):
        return '%s' % (self.app_name)
    # description.short_description = '比赛'
    # description.admin_order_field = 'id'

    def __unicode__(self):
        return self.description()

