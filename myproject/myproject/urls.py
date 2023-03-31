from django.urls import path
from .views import UploadCSVView, GetTop50View

urlpatterns = [
    path('upload_csv/', UploadCSVView.as_view(), name='upload_csv'),
    path('get_top_50/', GetTop50View.as_view(), name='get_top_50'),
]