from django.urls import path
from .views import NewsList, OnenewsDetail, PostList

urlpatterns = [
   path('', NewsList.as_view()),
   path('', PostList.as_view()),
   path('<int:id>', OnenewsDetail.as_view()),
]