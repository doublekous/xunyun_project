from django.conf.urls import url
from ip import views
from ip.views import Ip_queryView, Search_ipView, Upload_ipView, Continuous_ipView

urlpatterns = [
    url(r'^ip_query/$', Ip_queryView.as_view(), name='ip_query'),
    url(r'^search_ip/$', Search_ipView.as_view(), name='search_ip'),
    url(r'^export_ip/$', views.export_ip, name='export_ip'),
    url(r'^upload_ip/$', Upload_ipView.as_view(), name='upload_ip'),
    url(r'^continuous_ip/$', Continuous_ipView.as_view(), name='continuous_ip'),
]
