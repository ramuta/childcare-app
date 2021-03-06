from django.conf.urls import patterns, url
from classroom import views

urlpatterns = patterns('',
                       url(r'^classroom/create/$', views.classroom_create),
                       url(r'^classroom/(?P<classroom_id>\d+)/$', views.classroom),
                       url(r'^classroom/(?P<classroom_id>\d+)/children/$', views.classroom_children_section),

                       # diary
                       url(r'^classroom/(?P<classroom_id>\d+)/diary/$', views.diary_section),
                       url(r'^classroom/(?P<classroom_id>\d+)/diary/create/$', views.diary_create),
                       url(r'^classroom/(?P<classroom_id>\d+)/diary/(?P<diary_id>\d+)/$', views.diary_detail),

                       # attendance
                       url(r'^classroom/(?P<classroom_id>\d+)/attendance/$', views.attendance_section),
                       url(r'^classroom/(?P<classroom_id>\d+)/attendance/check/$', views.attendance_check),
                       url(r'^classroom/(?P<classroom_id>\d+)/attendance/(?P<attendance_id>\d+)/$', views.attendance_detail),
                       )