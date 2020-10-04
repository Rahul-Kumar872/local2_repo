from django.urls import path
from . import views

app_name='Blog'

urlpatterns = [
     path('', views.post_list, name='post_list'),
     #path('<int:pk>/', views.post_detail, name='post_detail'),
     path('<int:year>/<int:month>/<int:day>/<slug:post>/',
        views.post_detail,
        name='post_detail'),
     path('<int:id>/',views.mail_send_view),
     path('<tag_slug>/',views.post_list,name='post_list_by_tag_name')


]
