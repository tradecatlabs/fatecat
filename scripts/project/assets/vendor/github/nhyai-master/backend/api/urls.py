from django.urls import include, path
from rest_framework import routers
from api import views

router = routers.DefaultRouter()
router.register(r'users', views.UserViewSet)
router.register(r'groups', views.GroupViewSet)
router.register(r'uploads', views.FileUploadViewSet)
router.register(r'image/get_violence_identify', views.FileImageTerrorismUploadViewSet)
router.register(r'image/get_vision_porn', views.FileVisionPornUploadViewSet)
router.register(r'image/get_image_inspection', views.ImageFileUploadViewSet)
router.register(r'text/get_text_recognition', views.WordRecognitionViewSet)
router.register(r'text/get_text_recognition_inspection', views.WordRecognitionInspectionViewSet)
router.register(r'ocr/get_general_ocr', views.OcrGeneralViewSet)
router.register(r'ocr/get_idcard_ocr', views.OcrIDCardViewSet)
router.register(r'ocr/get_drivinglicense_ocr', views.OcrDrivinglicenseViewSet)
router.register(r'ocr/get_vehiclelicense_ocr', views.OcrVehiclelicenseViewSet)
router.register(r'ocr/get_bankcard_ocr', views.OcrBankcardViewSet)
router.register(r'ocr/get_handwritten_ocr', views.OcrHandWrittenViewSet)
router.register(r'ocr/get_vehicleplate_ocr', views.OcrVehicleplateViewSet)
router.register(r'audio/get_chinese_speech', views.AudioFileUploadViewSet)
router.register(r'audio/get_chinese_speech_inspection', views.AudioFileInspectionViewSet)
router.register(r'video/get_video_inspection', views.VideoFileUploadViewSet)
router.register(r'history/get_historyrecord_list', views.HistoryRecordListViewSet)
router.register(r'history/get_historyrecord_detail', views.HistoryRecordDetailViewSet)

image = routers.DefaultRouter()
image.register(r'get_violence_identify', views.FileImageTerrorismUploadViewSet)
image.register(r'get_vision_porn', views.FileVisionPornUploadViewSet)
image.register(r'get_image_inspection', views.ImageFileUploadViewSet)

text = routers.DefaultRouter()
text.register(r'get_text_recognition', views.WordRecognitionViewSet)
text.register(r'get_text_recognition_inspection', views.WordRecognitionInspectionViewSet)

ocr = routers.DefaultRouter()
ocr.register(r'get_general_ocr', views.OcrGeneralViewSet)
ocr.register(r'get_idcard_ocr', views.OcrIDCardViewSet)
ocr.register(r'get_drivinglicense_ocr', views.OcrDrivinglicenseViewSet)
ocr.register(r'get_vehiclelicense_ocr', views.OcrVehiclelicenseViewSet)
ocr.register(r'get_bankcard_ocr', views.OcrBankcardViewSet)
ocr.register(r'get_handwritten_ocr', views.OcrHandWrittenViewSet)
ocr.register(r'get_vehicleplate_ocr', views.OcrVehicleplateViewSet)

audio = routers.DefaultRouter()
audio.register(r'get_chinese_speech', views.AudioFileUploadViewSet)
audio.register(r'get_chinese_speech_inspection', views.AudioFileInspectionViewSet)

video = routers.DefaultRouter()
video.register(r'get_video_inspection', views.VideoFileUploadViewSet)

history = routers.DefaultRouter()
history.register(r'get_historyrecord_list', views.HistoryRecordListViewSet)
history.register(r'get_historyrecord_detail', views.HistoryRecordDetailViewSet)

# Wire up our API using automatic URL routing.
# Additionally, we include login URLs for the browsable API.
urlpatterns = [
    path('', include(router.urls)),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework')),
    path('image/', include(image.urls)),
    path('text/', include(text.urls)),
    path('ocr/', include(ocr.urls)),
    path('audio/', include(audio.urls)),
    path('video/', include(video.urls)),
    path('history/', include(history.urls))
]