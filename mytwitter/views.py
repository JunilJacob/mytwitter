from django.template.loader import get_template
from django.template import Context
from django.http import HttpResponse,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib import auth
from twitterapp.models import Post,Follow
from django.db.models import Q
#users home page
def mainpage(request):
	#if not an authenticted user redirect to login page
	if not request.user.is_authenticated():
		return HttpResponseRedirect("/account/login")
	else:
		status = request.GET.get('status')
		t = get_template('registration/home.html')
	#Get the list of users that authenticated user is following
		p = Follow.objects.get(username = request.user)
		follow = p.following.split(" ")
		try:
	#Retreiving the require posts
			entries = Post.objects.filter(username__in = follow).order_by('-created')[:10]
		except Post.DoesNotExist:
			if status:
				html = t.render(Context({ 'user' : request.user, 'entries' : None, 'message' : "User does not exist"}))
			else:
				html = t.render(Context({ 'user' : request.user, 'entries' : None, 'message' : ""}))
		else:
			if status:
				html = t.render(Context({ 'user' : request.user, 'entries' : entries, 'message' : "User does not exist"}))
			else:
				html = t.render(Context({ 'user' : request.user, 'entries' : entries, 'message' : ""}))

		return HttpResponse(html)
		

#check the login			
def logincheck(request):
	uname = request.POST.get('username')
	upass = request.POST.get('password')
	if uname and upass:
			try:
				user = User.objects.get(username = uname)
			except User.DoesNotExist:
	#if user does not exist redirect to login page with fail status
				return HttpResponseRedirect("/account/login?status=fail")
			else:
	#if user exist compare passwords
				if user.check_password(upass):
	#if passwords match authenticate user and redirect to home page
					user = auth.authenticate(username = uname, password = upass)
					if user is not None and user.is_active:
						auth.login(request, user)
						return HttpResponseRedirect("/?")
				else:
	#if password does not match redirect to login page with fail status
					return HttpResponseRedirect("/account/login?status=fail")
	else:
		return HttpResponseRedirect("/")		

#create a new user
def createuser(request):
	if request.method == 'POST':
		uname = request.POST.get('username')
		upass = request.POST.get('password')
		if uname and upass:
			try:
				user = User.objects.get(username=uname)
			except User.DoesNotExist:
	#if user does not exist create user and redirect the authetiicated user to homepage
				user = User.objects.create_user(username = uname,password = upass)
				user.save()
				user = Follow(username = uname,following = uname)
				user.save()
				user = auth.authenticate(username = uname, password = upass)
				if user is not None and user.is_active:
					auth.login(request, user)
				return HttpResponseRedirect("/")
			else:
	#if user already exist redirect to signup page with fail status
				return HttpResponseRedirect("/account/create?status=fail")
	else:
	#display signup page if GET method is used
		status = request.GET.get('status')
		t = get_template('registration/signup.html')
		if status:
			html = t.render(Context({'message' : "Username already exists"}))
		else:
			html = t.render(Context({'message' : ""}))
		return HttpResponse(html)

#login page
def login(request):
	#if user is authenticated redirect to home page
	if request.user.is_authenticated():
		return HttpResponseRedirect("/")
	#else show login page
	status = request.GET.get('status')
	t = get_template('registration/login.html')
	if status:
		html = t.render(Context({'message' : "Invalid user name or Password"}))
	else:
		html = t.render(Context({'message' : ""}))
	return HttpResponse(html)

#logout user
def logout(request):
	auth.logout(request)
	return HttpResponseRedirect("/")

#Save new post to database
def newpost(request):
	if request.method == 'POST':
		data = request.POST.get('postdata')
		user = request.user
		p = Post(username = user, post = data)
		p.save()
		return HttpResponseRedirect("/")

#follow a user
def follow(request):
	followuser=request.GET.get('user')
	users=Follow.objects.filter(username=request.user)[0].following.split(" ")
	users.append(str(followuser))
	p=Follow.objects.filter(username=request.user)[0]
	p.following=" ".join(users)
	p.save()
	return HttpResponseRedirect("/")

#search for a user
def search(request):
	searchuser=request.GET.get('searchuser')
	usersfollowing=Follow.objects.filter(username=request.user)[0].following.split(" ")
	usersnotfollowing=Follow.objects.filter(~Q(username__in = usersfollowing))
	if searchuser:
		usersnotfollowing=Follow.objects.filter(~Q(username__in = usersfollowing) & Q(username__regex=searchuser))
		t = get_template('registration/search.html')
		html = t.render(Context({'user' : request.user, 'entries': usersnotfollowing}))
		return HttpResponse(html)
	else:
		usersnotfollowing=Follow.objects.filter(~Q(username__in = usersfollowing))
		t = get_template('registration/search.html')
		html = t.render(Context({'user' : request.user, 'entries': usersnotfollowing}))
		return HttpResponse(html)

#show the list of users that we are following
def following(request):
	usersfollowing=Follow.objects.filter(username=request.user)[0].following.split(" ")
	usersfollowing.remove(str(request.user))
	users=Follow.objects.filter(username__in = usersfollowing)
	t = get_template('registration/following.html')
	html = t.render(Context({'user' : request.user,'entries':users}))
	return HttpResponse(html)

#unfollow a user
def unfollow(request):
	unfollowuser=request.GET.get('user')
	users=Follow.objects.filter(username=request.user)[0].following.split(" ")
	users.remove(unfollowuser)
	p=Follow.objects.filter(username=request.user)[0]
	p.following=" ".join(users)
	p.save()
	return HttpResponseRedirect("/following")
	
