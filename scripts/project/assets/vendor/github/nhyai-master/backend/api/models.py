from django.db import models
from django.contrib.auth.models import User
from rest_framework import serializers
from django.utils.timezone import datetime
from uuid import uuid4
import os
from django.utils.translation import gettext_lazy as _
from sortedm2m.fields import SortedManyToManyField
# Create your models here.


def path_and_rename(instance, filename):
    upload_to = 'photos'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def audiopath_and_rename(instance, filename):
    upload_to = 'audios'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def video_and_rename(instance, filename):
    upload_to = 'videos'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


def text_and_rename(instance, filename):
    upload_to = 'text'
    ext = filename.split('.')[-1]
    # get filename
    if instance.pk:
        filename = '{}.{}'.format(instance.pk, ext)
    else:
        # set filename as random string
        filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class FileUpload(models.Model):
    # datafile = models.ImageField(upload_to='photos')
    datafile = models.ImageField(
        upload_to=path_and_rename, max_length=255, null=True, blank=True)
    result = models.TextField(max_length=256, default='')


class FileImageTerrorismUpload(models.Model):
    # datafile = models.ImageField(upload_to='photos')
    # datafile = models.ImageField(upload_to=path_and_rename, max_length=255, null=True, blank=True)
    # result1 = models.TextField(max_length=256,default='')
    image = models.FileField(upload_to=path_and_rename,
                             max_length=255, null=True, blank=True)
    image_url = models.URLField(_('image_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')


class FileVisionPornUpload(models.Model):
    # datafile = models.ImageField(upload_to='photos')
    image = models.ImageField(
        upload_to=path_and_rename, max_length=255, null=True, blank=True)
    image_url = models.URLField(_('image_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=256, default='')


class WordRecognition(models.Model):
    text = models.CharField(_('text'), max_length=1530, null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    sensitive_hit_flag = models.IntegerField(
        _('sensitive_hit_flag'), null=True, blank=True)
    sensitive_size = models.IntegerField(
        _('sensitive_size'), null=True, blank=True)
    sensitive_list = models.TextField(max_length=1024, default='')
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')


class WordRecognitionInspection(models.Model):
    text = models.FileField(upload_to=text_and_rename,
                            max_length=1530, null=True, blank=True)
    text_url = models.URLField(_('text_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')


class OcrGeneral(models.Model):
    image = models.ImageField(
        upload_to=path_and_rename, max_length=255, null=True, blank=True)
    image_url = models.URLField(_('image_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=255, default='')


class OcrIDCard(models.Model):
    image = models.ImageField(
        upload_to=path_and_rename, max_length=255, null=True, blank=True)
    image_url = models.URLField(_('image_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')


class VideoFileUpload(models.Model):
    # datafile = models.ImageField(upload_to='photos')
    video = models.FileField(upload_to=video_and_rename,
                             max_length=255, null=True, blank=True)
    video_url = models.URLField(_('video_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')


class AudioFileUpload(models.Model):
    # datafile = models.ImageField(upload_to='photos')
    speech = models.FileField(
        upload_to=audiopath_and_rename, max_length=255, null=True, blank=True)
    speech_url = models.URLField(_('speech_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')


class AudioFileInspection(models.Model):
    # datafile = models.ImageField(upload_to='photos')
    speech = models.FileField(
        upload_to=audiopath_and_rename, max_length=255, null=True, blank=True)
    speech_url = models.URLField(_('speech_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')


class ImageFileUpload(models.Model):
    # datafile = models.ImageField(upload_to='photos')
    image = models.ImageField(
        upload_to=path_and_rename, max_length=255, null=True, blank=True)
    image_url = models.URLField(_('image_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=256, default='')


class OcrDrivinglicense(models.Model):
    image = models.ImageField(
        upload_to=path_and_rename, max_length=255, null=True, blank=True)
    image_url = models.URLField(_('image_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')


class OcrVehiclelicense(models.Model):
    image = models.ImageField(
        upload_to=path_and_rename, max_length=255, null=True, blank=True)
    image_url = models.URLField(_('image_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')


class OcrBankcard(models.Model):
    image = models.ImageField(
        upload_to=path_and_rename, max_length=255, null=True, blank=True)
    image_url = models.URLField(_('image_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')


class OcrHandWritten(models.Model):
    image = models.ImageField(
        upload_to=path_and_rename, max_length=255, null=True, blank=True)
    image_url = models.URLField(_('image_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')


class OcrVehicleplate(models.Model):
    image = models.ImageField(
        upload_to=path_and_rename, max_length=255, null=True, blank=True)
    image_url = models.URLField(_('image_url'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, default='')
    data = models.TextField(max_length=2048, default='')

class SensitivityType(models.Model):
    sensitivity_type = models.CharField(
        _('sensitivity_type'), max_length=32, null=True, blank=True)


class SensitivityLevel(models.Model):
    sensitivity_level = models.CharField(
        _('sensitivity_level'), max_length=4, null=True, blank=True)


class HistoryRecord(models.Model):
    file_id = models.CharField(
        _('file_id'), max_length=32, null=True, blank=True)
    file_name = models.CharField(
        _('file_name'), max_length=128, null=True, blank=True)
    file_url = models.URLField(_('image_url'), null=True, blank=True)
    file_type = models.IntegerField(_('file_type'), null=True, blank=True)
    inspection_result = models.CharField(
        _('inspection_result'), max_length=32, null=True, blank=True)
    max_sensitivity_type = models.CharField(
        _('max_sensitivity_type'), max_length=32, null=True, blank=True)
    max_sensitivity_level = models.CharField(
        _('max_sensitivity_level'), max_length=4, null=True, blank=True)
    sensitivity_types = SortedManyToManyField(SensitivityType, blank=True)
    sensitivity_levels = SortedManyToManyField(SensitivityLevel, blank=True)
    violence_percent = models.CharField(
        _('violence_percent'), max_length=16, null=True, blank=True)
    violence_sensitivity_level = models.CharField(
        _('violence_sensitivity_level'), max_length=4, null=True, blank=True)
    porn_percent = models.CharField(
        _('porn_percent'), max_length=16, null=True, blank=True)
    porn_sensitivity_level = models.CharField(
        _('porn_sensitivity_level'), max_length=4, null=True, blank=True)
    politics_percent = models.CharField(
        _('politics_percent'), max_length=16, null=True, blank=True)
    politics_sensitivity_level = models.CharField(
        _('politics_sensitivity_level'), max_length=4, null=True, blank=True)
    public_percent = models.CharField(
        _('public_percent'), max_length=16, null=True, blank=True)
    public_character_level = models.CharField(
        _('public_character_level'), max_length=4, null=True, blank=True)
    content = models.CharField(_('content'), max_length=1530, null=True, blank=True)
    upload_time = models.DateTimeField(auto_now=True, null=True, blank=True)
    process_status = models.IntegerField(_('process_status'), null=True, blank=True)
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, null=True, default='')
    data = models.TextField(max_length=2048, null=True, default='')

class HistoryRecordList(models.Model):
    system_id = models.IntegerField(_('system_id'), null=True, blank=True)
    channel_id = models.IntegerField(_('channel_id'), null=True, blank=True)
    user_id = models.CharField(
        _('user_id'), max_length=64, null=True, blank=True)
    begin_time = models.DateTimeField(auto_now=True, blank=True)
    end_time = models.DateTimeField(auto_now=True, blank=True)
    file_name = models.CharField(
        _('file_name'), max_length=128, null=True, blank=True)
    file_type = models.IntegerField(_('file_type'), null=True, blank=True)
    current_page = models.IntegerField(_('current_page'), null=True, blank=True)
    page_size = models.IntegerField(_('page_size'), null=True, blank=True)
    history_records = SortedManyToManyField(HistoryRecord, blank=True)
    ret = models.IntegerField(_('ret'), null=True, blank=True)
    msg = models.TextField(max_length=255, null=True, default='')
    data = models.TextField(max_length=2048, null=True, default='')