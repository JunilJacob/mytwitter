from django.conf.urls import patterns, include, url
from views import mainpage,logincheck,login,logout,createuser
urlpatterns = patterns('',(r'^$', mainpage),
    (r'^account/create$', createuser),
    (r'^account/login$',  login),
    (r'^account/logout$', logout),
	(r'^account/login/check',logincheck),
)
