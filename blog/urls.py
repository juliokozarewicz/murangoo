from django.urls import path
from .views import blog, post_detail_content


app_name = 'blog'

urlpatterns = [
    path('blog/', blog.as_view(), name='blog'),
    path('post/<slug:slug>', post_detail_content.as_view(), name='post_detail_content'),
]