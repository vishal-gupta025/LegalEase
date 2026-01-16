from django.urls import path
from .views import AskQuestionApi, LoginApi, RegisterApi, UploadDocumentAPI
urlpatterns = [
    path('ask/', AskQuestionApi.as_view(), name='ask-question'),
    path('upload-document/', UploadDocumentAPI.as_view(), name='upload-document'),
    path('register/', RegisterApi.as_view(), name='register'),
    path('login/', LoginApi.as_view(), name='login'),
]