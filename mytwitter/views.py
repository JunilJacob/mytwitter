from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from twitterapp.models import Post,Follow
from django.db.models import Q
import re
def template_rendering(path):
	t = get_template(path)
	html = t.render(Context({}))
	return html

def mainpage(request):
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/account/login")
	else:
		t = get_template('registration/home.html')
		p = Follow.objects.get(username=request.user)
		follow = p.following.split(" ")
		try:
			entries = Post.objects.filter(username__in=follow).order_by('-created')
		except Post.DoesNotExist:
			t.render(Context({ 'user' : request.user,'entries': None}))
		else:
			html = t.render(Context({ 'user' : request.user,'entries':entries}))
		return HttpResponse(html)
		
			
def logincheck(request):
	uname = request.POST.get('username')
	upass = request.POST.get('password')
	if uname and upass:
			try:
				user = User.objects.get(username=uname)
			except User.DoesNotExist:
				return HttpResponseRedirect("/account/login")
			else:
				if user.check_password(upass):
					user = auth.authenticate(username=uname, password=upass)
					if user is not None and user.is_active:
						auth.login(request, user)
						return HttpResponseRedirect("/")
				else:
					return HttpResponseRedirect("/account/login")
	else:
		return HttpResponseRedirect("/")		
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
				user = Follow(username = uname,following = uname)
				user.save()
				user = auth.authenticate(username=uname, password=upass)
				if user is not None and user.is_active:
					auth.login(request, user)
				return HttpResponseRedirect("/")
			else:
				return HttpResponseRedirect("/account/create")
	else:
				html=template_rendering('registration/signup.html')
				return HttpResponse(html)

def login(request):
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	t = get_template('registration/login.html')
	html = t.render(Context({}))
	return HttpResponse(html)

def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")

def newpost(request):
	if request.method == 'POST':
		data = request.POST.get('postdata')
		user = request.user
		p = Post(username = user, post = data)
		p.save()
		return HttpResponseRedirect("/")
def follow(request):
	if request.method == 'POST':
		followuser = request.POST.get('follow')
		try:
			p = Follow.objects.get(username=followuser)
		except Follow.DoesNotExist:
			return HttpResponseRedirect("/")
		else:
			p = Follow.objects.get(username=request.user)
			p.following=p.following	+ " " +	str(followuser)
			p.save()
			return HttpResponseRedirect("/")
