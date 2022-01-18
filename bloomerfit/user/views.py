from django.shortcuts import  render, redirect
from user.forms import AuthenticationForm, FitnessMeterForm, NewUserCreationForm, NewUserChangeForm, WeightMetricForm, HeightMetricForm, WeightTrackForm, ContactForm
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponseRedirect
from .models import StatsLogin, User, Contact
from django.urls import reverse
from decimal import Decimal

def index(request):
	return render(request, 'user/index.html')
    
def members(request):
	if not request.user.is_authenticated:
		return HttpResponseRedirect(reverse("user:login"))
	if request.user:
		u=User.objects.get(email=request.user.email)
		gender=u.gender
		weight=u.weight
		height=u.height
		waist=u.waist
		hips=u.hips
		bmi = weight/height**2
		whr = waist/hips
		heightSquared = height**2
		weightShouldBe_one = round(19 * heightSquared)
		weightShouldBe_two = round(24 * heightSquared)
		context={
			'gender':gender, 'weight':weight, 'height':height, 'waist':waist, 'hips':hips, 'bmi':bmi, 'whr':whr, 'weightShouldBe_one':weightShouldBe_one, 'weightShouldBe_two':weightShouldBe_two
		}
		return render(request, "user/members.html", context)
	else:
		return redirect('user/login')    

def signup(request):
	if request.method == "POST":
		form = NewUserCreationForm(request.POST)
		if form.is_valid():
			user = form.save()
			login(request, user)
			messages.success(request, "Registration successful. Welcome to BloomerFit. You are now a member of the family.")
			return redirect("user:login")
		messages.error(request, "Unsuccessful registration. Invalid information.")
	form = NewUserCreationForm()
	return render (request=request, template_name="user/signup.html", context={"form":form})

def login_request(request):
	if request.method == "POST":
		form = AuthenticationForm(request.POST)
		if form.is_valid():
			email = form.cleaned_data.get('email')
			password = form.cleaned_data.get('password')
			user = authenticate(email=email, password=password)
			if user is not None:
				login(request, user)
				#messages.info(request, f"You are now logged in as {email}.")
				return redirect("user:members")
			else:
				messages.error(request,"Invalid email or password.")
		else:
			messages.error(request,"Invalid email or password.")
	form = AuthenticationForm()
	return render(request, "user/login.html", {"form":form})

def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("user:login")

def fitnessMeter(request):
	if request.method=="POST":
		form=FitnessMeterForm(request.POST)
		if form.is_valid():
			name = form.cleaned_data['name']
			weight = form.cleaned_data['weight']
			weightunit = form.cleaned_data['weightunit']
			height=form.cleaned_data['height']
			waist=form.cleaned_data['waist']
			hips=form.cleaned_data['hips']
			gender=form.cleaned_data['gender']
			
			if weightunit == "kg":
				weight = weight
			else:
				weight = weight * Decimal(0.454)
				weight = round(weight, 2)

			# Convert height to meter
			height = height/100

			# Get BMI and WHR
			bmi = weight/(height**2)
			bmi = round(bmi, 2)
			whr = waist/hips
			whr = round(whr, 2)

            # Get ideal weight
			heightSquared = height**2
			weightShouldBe_one = round(19 * heightSquared)
			weightShouldBe_two = round(24 * heightSquared)
			min_weight_loss = round(weight - weightShouldBe_two, 1)

			return render(request, "user/result.html", {'name':name,'bmi':bmi, 'whr':whr,'weightShouldBe_one':weightShouldBe_one,
								'weightShouldBe_two':weightShouldBe_two, 'gender':gender,
								'min_weight_loss':min_weight_loss} )
	form=FitnessMeterForm()
	return render(request, "user/fitnessMeter.html", {'form':form})	



@login_required
def profile(request):
	u = User.objects.get(email=request.user.email)
	log=StatsLogin()
	if request.method=="POST":
		form=NewUserChangeForm(request.POST)
		if form.is_valid():
			weight=form.cleaned_data['weight']
			height=form.cleaned_data['height']
			waist=form.cleaned_data['waist']
			hips=form.cleaned_data['hips']

			# Process the user data from the form submitted
			
			bmi=weight/height**2
			bmi=round(bmi, 2)
			whr=waist/hips
			whr= round(whr, 2)
            
            #https://developer.mozilla.org/en-US/docs/Learn/Server-side/Django/Forms

			# Store info in database
            # ...starting by updating the User table 
			u.weight=weight
			u.height=height
			u.waist=waist
			u.hips=hips
			u.save()

			# ... and then log in the user's stats into the StatsLogin table
			log.weight=weight
			log.height=height
			log.waist=waist
			log.hips=hips
			log.person=u
			log.save()

			# Get the user's gender from the User table , 'weight':weight
			gender=u.gender

			# Query the database for all the stats the user 'u' as logged in, starting with the most recent ones.
			user_stats = u.statslogin_set.all().order_by('-time')

			return render(request, "user/userProfile.html", {'bmi':bmi, 'whr':whr, 'user_stats': user_stats})
			
	form = NewUserChangeForm()
	weight=u.weight
	height=u.height
	waist=u.waist
	hips=u.hips
	return render(request, "user/profile.html", {'form':form, 'weight':weight, 'height':height, 'waist':waist, 'hips':hips })

def m_converter(request):
	return render(request, "user/m_converter.html")

def metric_converter(request):
	if request.method=="POST":
		weight_form=WeightMetricForm(request.POST)
		
		if weight_form.is_valid():
			weight=weight_form.cleaned_data["weight"]
			
			# Convert weight to Kilogram
			weight = weight * Decimal(0.454)
			weight = round(weight, 2)
			
			context={
				"weight":weight,	
			}
			return render(request, "user/metric_converter.html", context)
	weight_form = WeightMetricForm()
	
	return render(request, "user/metric_converter.html", {"weight_form":weight_form})

def metric_converter_two(request):
	if request.method=="POST":
		height_form=HeightMetricForm(request.POST)
		
		if height_form.is_valid():		
			height=height_form.cleaned_data["height"]
			height2=height_form.cleaned_data["height2"]
			if height2 is None:
				height2=0
			
			height2Ft = height2 / 12
			height_in_meter=(height + height2Ft) * Decimal(0.3048)
			height_in_meter = round(height_in_meter, 2)
			height_in_cm = height_in_meter * 100
			
			return render(request, "user/metric_converter_two.html", {"height_in_meter":height_in_meter, "height_in_cm":height_in_cm })
	height_form = HeightMetricForm()
	
	return render(request, "user/metric_converter_two.html", {"height_form":height_form})

@login_required
def weight_tracker(request):
	u = User.objects.get(email=request.user.email)
	weight=u.weight
	height=u.height
	heightSquared = height**2
	weightShouldBe_one = round(19 * heightSquared)
	form = WeightTrackForm()
	
	if request.method=="POST":
		form=WeightTrackForm(request.POST) 
		if form.is_valid():
			desired_weight=form.cleaned_data["desired_weight"]
			if desired_weight >= weight:
				messages.error(request,"You shouldn't set a target greater than your current weight.")
			elif desired_weight < weightShouldBe_one:
				messages.error(request,"You dey whine? You've set a target way too low.")
			min_time_to_get_result= weight - desired_weight 
			min_time_to_get_result_days = min_time_to_get_result * Decimal(7) 
			min_time_to_get_result_days = round(min_time_to_get_result_days)
			max_time_to_get_result_days = min_time_to_get_result_days * 2
			if min_time_to_get_result_days >= 30:
				min_month= int(min_time_to_get_result_days/30)
				days_left=min_time_to_get_result_days % 30
			else:
				min_month = 0
				days_left = min_time_to_get_result_days
			return render(request, "user/weight_tracker.html", {'min_time_to_get_result_days':min_time_to_get_result_days, 'max_time_to_get_result_days':max_time_to_get_result_days, 'weight':weight, 'desired_weight':desired_weight, 'weightShouldBe_one':weightShouldBe_one, 'min_month':min_month, 'days_left':days_left})		
	return render(request, "user/weight_tracker.html", {'form': form, 'weight':weight})
	
def contact(request):
    if request.method == 'POST':
        form=ContactForm(request.POST)
        if form.is_valid():
            contact = Contact(
                author=form.cleaned_data["author"],
				email =form.cleaned_data["email"],
                body=form.cleaned_data["body"],
            )
            contact.save()
            messages.info(request, f"Thanks, we have received your message. We'll get back to you soon.")
    form = ContactForm()	
    return render(request, "user/contact.html", {"form":form})






