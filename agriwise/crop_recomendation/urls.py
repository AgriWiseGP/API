from django.urls import path
from .views import CropsGetAPIView, CropRecommendationPostListAPIView,CropGetDeleteApi

urlpatterns = [
    path('crop/', CropRecommendationPostListAPIView.as_view(), name='crop_recommendations_list_post'),
    path('<str:username>/crops/', CropsGetAPIView.as_view(), name='user_crop_recommendation_list'),
    path('<str:username>/crops/<int:crop_id>/', CropGetDeleteApi.as_view(), name='user_crop_recommendation_list'),

]
