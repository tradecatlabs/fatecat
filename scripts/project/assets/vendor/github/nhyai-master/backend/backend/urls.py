"""backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path,include
from django.views.generic import TemplateView
from django.conf.urls.static import static
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', TemplateView.as_view(template_name="index.html")),
    path('sindex', TemplateView.as_view(template_name="index.html")),
    path('imageRecognition', TemplateView.as_view(template_name="index.html")),
    path('yellow', TemplateView.as_view(template_name="index.html")),
    path('force', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/idCard', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/drivingLicence', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/vehicleLicence', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/bankcard', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/vehicleplate', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/runningLicence', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/commonUse', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/businessLicence', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/bankCard', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/handwriten', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/carNumber', TemplateView.as_view(template_name="index.html")),
    path('wordRecognition/visitingCard', TemplateView.as_view(template_name="index.html")),
    path('voiceRecognition', TemplateView.as_view(template_name="index.html")),
    path('writeRecognition', TemplateView.as_view(template_name="index.html")),
    path('videoRecognition', TemplateView.as_view(template_name="index.html")),
    path('api/v1/', include('api.urls'))
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)