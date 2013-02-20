from django.conf.urls import patterns, include, url
from views import mainpage,logincheck,login,logout,createuser,newpost,follow
urlpatterns = patterns('',(r'^$', mainpage),
	(r'^post/new', newpost),
    (r'^account/create$', createuser),
    (r'^account/login$',  login),
    (r'^account/logout$', logout),
	(r'^account/login/check',logincheck),
	(r'follow',follow)
)
