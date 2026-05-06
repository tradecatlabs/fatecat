from django.contrib.auth.models import User, Group
from rest_framework import serializers
from .models import FileUpload, FileImageTerrorismUpload, FileVisionPornUpload
from .models import VideoFileUpload, AudioFileUpload, AudioFileInspection, ImageFileUpload, WordRecognitionInspection
from .models import WordRecognition, OcrGeneral, OcrIDCard, OcrDrivinglicense, OcrVehiclelicense, OcrBankcard, HistoryRecord, HistoryRecordList


class UserSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = User
        fields = ('url', 'username', 'email', 'groups')


class GroupSerializer(serializers.HyperlinkedModelSerializer):
    class Meta:
        model = Group
        fields = ('url', 'name')


class FileUploadSerializer(serializers.HyperlinkedModelSerializer):

    result = serializers.JSONField(True)

    class Meta:
        model = FileUpload
        fields = ('datafile', 'result')

    def clean_json(self, obj):
        return obj.result


class WordRecognitionSerializer(serializers.HyperlinkedModelSerializer):

    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = WordRecognition
        fields = ('text', 'system_id', 'channel_id',
                  'user_id', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class WordRecognitionInspectionSerializer(serializers.HyperlinkedModelSerializer):

    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = WordRecognitionInspection
        fields = ('text', 'system_id', 'channel_id',
                  'user_id', 'text_url', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class OcrGeneralSerializer(serializers.HyperlinkedModelSerializer):

    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = OcrGeneral
        fields = ('image', 'image_url', 'system_id',
                  'channel_id', 'user_id', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class OcrIDCardSerializer(serializers.HyperlinkedModelSerializer):

    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = OcrIDCard
        fields = ('image', 'image_url', 'system_id',
                  'channel_id', 'user_id', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class FileImageTerrorismUploadSerializer(serializers.HyperlinkedModelSerializer):
    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = FileImageTerrorismUpload
        fields = ('image', 'image_url', 'system_id',
                  'channel_id', 'user_id', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class FileVisionPornUploadSerializer(serializers.HyperlinkedModelSerializer):
    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = FileVisionPornUpload
        #fields = ('datafile', 'result')
        fields = ('image', 'image_url', 'system_id',
                  'channel_id', 'user_id', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class VideoFileUploadSerializer(serializers.HyperlinkedModelSerializer):

    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = VideoFileUpload
        fields = ('video', 'video_url', 'system_id',
                  'channel_id', 'user_id', 'data', 'ret', 'msg')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class AudioFileUploadSerializer(serializers.HyperlinkedModelSerializer):

    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = AudioFileUpload
        fields = ('speech', 'speech_url', 'system_id',
                  'channel_id', 'user_id', 'data', 'ret', 'msg')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class AudioFileInspectionSerializer(serializers.HyperlinkedModelSerializer):

    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = AudioFileInspection
        fields = ('speech', 'speech_url', 'system_id',
                  'channel_id', 'user_id', 'data', 'ret', 'msg')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class ImageFileUploadSerializer(serializers.HyperlinkedModelSerializer):
    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = ImageFileUpload
        #fields = ('datafile', 'result')
        fields = ('image', 'image_url', 'system_id',
                  'channel_id', 'user_id', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class OcrDrivinglicenseSerializer(serializers.HyperlinkedModelSerializer):

    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = OcrDrivinglicense
        fields = ('image', 'image_url', 'system_id',
                  'channel_id', 'user_id', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class OcrVehiclelicenseSerializer(serializers.HyperlinkedModelSerializer):

    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = OcrVehiclelicense
        fields = ('image', 'image_url', 'system_id',
                  'channel_id', 'user_id', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class OcrBankcardSerializer(serializers.HyperlinkedModelSerializer):

    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = OcrBankcard
        fields = ('image', 'image_url', 'system_id',
                  'channel_id', 'user_id', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class OcrHandWrittenSerializer(serializers.HyperlinkedModelSerializer):

    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = OcrBankcard
        fields = ('image', 'image_url', 'system_id',
                  'channel_id', 'user_id', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class OcrVehicleplateSerializer(serializers.HyperlinkedModelSerializer):

    #result = serializers.JSONField(True)
    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = OcrBankcard
        fields = ('image', 'image_url', 'system_id',
                  'channel_id', 'user_id', 'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class HistoryRecordListSerializer(serializers.HyperlinkedModelSerializer):

    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)

    class Meta:
        model = HistoryRecordList
        fields = ('system_id', 'channel_id', 'user_id',
                  'begin_time', 'end_time', 'file_name',
                  'file_type', 'current_page', 'page_size',
                  'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data


class HistoryRecordDetailSerializer(serializers.HyperlinkedModelSerializer):

    ret = serializers.JSONField(True)
    msg = serializers.JSONField(True)
    data = serializers.JSONField(True)
    file_id = serializers.JSONField(True)
    file_name = serializers.JSONField(True)
    file_url = serializers.JSONField(True)
    file_type = serializers.JSONField(True)
    inspection_result = serializers.JSONField(True)
    max_sensitivity_type = serializers.JSONField(True)
    max_sensitivity_level = serializers.JSONField(True)
    violence_percent = serializers.JSONField(True)
    violence_sensitivity_level = serializers.JSONField(True)
    porn_percent = serializers.JSONField(True)
    porn_sensitivity_level = serializers.JSONField(True)
    politics_percent = serializers.JSONField(True)
    politics_sensitivity_level = serializers.JSONField(True)
    public_percent = serializers.JSONField(True)
    public_character_level = serializers.JSONField(True)
    content = serializers.JSONField(True)
    upload_time = serializers.JSONField(True)
    process_status = serializers.JSONField(True)
    system_id = serializers.JSONField(True)
    channel_id = serializers.JSONField(True)
    user_id = serializers.JSONField(True)

    class Meta:
        model = HistoryRecord
        fields = ('id', 'file_id', 'file_name', 'file_url',
                  'file_type', 'inspection_result', 'max_sensitivity_type',
                  'max_sensitivity_level', 'violence_percent', 'violence_sensitivity_level',
                  'porn_percent', 'porn_sensitivity_level', 'politics_percent',
                  'politics_sensitivity_level', 'public_percent', 'public_character_level',
                  'content', 'upload_time', 'process_status', 'system_id',
                  'channel_id', 'user_id',
                  'ret', 'msg', 'data')

    def clean_json(self, obj):
        return obj.ret, obj.msg, obj.data, obj.file_id, obj.file_name, obj.file_url,
        obj.file_type, obj.inspection_result, obj.max_sensitivity_type,
        obj.max_sensitivity_level, obj.violence_percent, obj.violence_sensitivity_level,
        obj.porn_percent, obj.porn_sensitivity_level, obj.politics_percent,
        obj.politics_sensitivity_level, obj.public_percent, obj.public_character_level,
        obj.content, obj.upload_time, obj.process_status, obj.system_id,
        obj.channel_id, obj.user_id
