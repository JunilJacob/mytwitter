from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
def template_rendering(path):
	t = get_template(path)
	html = t.render(Context({}))
	return html

def mainpage(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/account/login")
	else:
		t = get_template('registration/home.html')
		html = t.render(Context({ 'user' : request.user}))
		return HttpResponse(html)
def logincheck(request):
	uname = request.POST.get('username')
	upass = request.POST.get('password')
	if uname and upass:
			try:
				user = User.objects.get(username=uname)
			except User.DoesNotExist:
				html=template_rendering('registration/login.html')
				return HttpResponse(html)
			else:
				if user.check_password(upass):
					user = auth.authenticate(username=uname, password=upass)
					if user is not None and user.is_active:
						auth.login(request, user)
					return HttpResponseRedirect("/")
				else:
					html=template_rendering('registration/login.html')
					return HttpResponse(html)
def createuser(request):
	if request.method == 'POST':
		uname = request.POST.get('username')
		upass = request.POST.get('password')
		if uname and upass:
			try:
				user = User.objects.get(username=uname)
			except User.DoesNotExist:
				user = User.objects.create_user(username = uname,password = upass)
				user.save()
				html=template_rendering('registration/login.html')
				return HttpResponse(html)
			else:
				html=template_rendering('registration/signup.html')
				return HttpResponse(html)
	else:
				html=template_rendering('registration/signup.html')
				return HttpResponse(html)

def login(request):
	html=template_rendering('registration/login.html')
	return HttpResponse(html)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")

