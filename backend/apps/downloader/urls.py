from django.urls import path

from downloader.views import DownloaderView


app_name = 'downloader'

urlpatterns = [
    path('', DownloaderView.as_view(), name = 'download'),
]