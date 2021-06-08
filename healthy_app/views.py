from django.shortcuts import render, HttpResponse, redirect
from django.contrib import messages
from . models import User, Food, Workout, Weight
import bcrypt

#DISPLAYS
def index(request):
    return render(request, 'index.html')

def dashboard(request):
    if "user_id" not in request.session:
        return redirect("/")
    context = {
        "user": User.objects.get(id=int(request.session["user_id"])),
        "allfood": Food.objects.all().order_by('-updated_at'),
        "allworkout": Workout.objects.all().order_by('-updated_at'),
        "allweight": Weight.objects.all().order_by('-created_at'),
        }
    return render(request, "dashboard.html", context)

def newfoods(request): 
    if "user_id" not in request.session:
        return redirect("/")
    else:
        context = {
            "user": User.objects.get(id=int(request.session["user_id"])),
        }
        return render(request, "food.html", context)

def newworkout(request): 
    if "user_id" not in request.session:
        return redirect("/")
    else:
        context = {
            "user": User.objects.get(id=int(request.session["user_id"])),
        }
        return render(request, "workout.html", context)

def weighin(request): 
    if "user_id" not in request.session:
        return redirect("/")
    else:
        context = {
            "user": User.objects.get(id=int(request.session["user_id"])),
        }
        return render(request, "weight.html", context)

def viewall(request):
    if "user_id" not in request.session:
        return redirect("/")
    else:
        context = {
            "user": User.objects.get(id=int(request.session["user_id"])),
            "allfood": Food.objects.all().order_by('-updated_at'),
            "allworkout": Workout.objects.all().order_by('-updated_at'),
            "allweight": Weight.objects.all().order_by('-created_at'),
        }
        return render(request, "allinfo.html", context)


########################################################################
########################################################################

#ACTIONS
def regi(request):
    # if "user_id" not in request.session:
    #     return redirect("/")
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0: 
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        hashed_pw = bcrypt.hashpw(request.POST["Password"].encode(), bcrypt.gensalt()).decode()
        new_regi = User.objects.create(first_name=request.POST["f_name"], last_name=request.POST["l_name"], email=request.POST["Email"], password=hashed_pw)
        request.session["user_id"] = new_regi.id 
        return redirect("/dashboard")

def create(request):
    if "user_id" not in request.session:
        return redirect("/")
    errors = Food.objects.food_validator(request.POST)
    if len(errors) > 0: 
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/food/new/")
    else:
        logged_user = User.objects.get(id=int(request.session["user_id"]))
        food_entry = Food.objects.create(food_item=request.POST["food"], meal_type=request.POST["food_type"], user=logged_user)
        return redirect("/dashboard")

def create_workout(request):
    if "user_id" not in request.session:
        return redirect("/")
    errors = Workout.objects.workout_validator(request.POST)
    if len(errors) > 0: 
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/workout/new")
    else:
        logged_user = User.objects.get(id=int(request.session["user_id"]))
        workout_entry = Workout.objects.create(workout_type=request.POST["workout"], time=request.POST["time"], user=logged_user)
        return redirect("/dashboard")

def create_weighin(request):
    if "user_id" not in request.session:
        return redirect("/")
    errors = Weight.objects.weight_validator(request.POST)
    if len(errors) > 0: 
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/weigh-in/new")
    else:
        logged_user = User.objects.get(id=int(request.session["user_id"]))
        weighin_entry = Weight.objects.create(weight=request.POST["weight"], user=logged_user)
        return redirect("/dashboard")


def editfood(request, foodid):
    if "user_id" not in request.session:
        return redirect("/")
    errors = Food.objects.food_validator(request.POST)
    if len(errors) > 0: 
        for key, value in errors.items():
            messages.error(request, value)
        return redirect(f"/food/{foodid}/edit")
    else:
        logged_user = User.objects.get(id=int(request.session["user_id"]))
        food = Food.objects.get(id=foodid)
        food.meal_type = request.POST["meal_type"]
        food.food_item = request.POST["food_item"]
        food.save()
        return redirect("/dashboard")

def food_destroy(request, foodid):
    if "user_id" not in request.session:
        return redirect("/")
    deletefood = Food.objects.get(id=foodid)
    deletefood.delete()
    return redirect("/dashboard")

def workout_destroy(request, workoutid):
    if "user_id" not in request.session:
        return redirect("/")
    deleteworkout = Workout.objects.get(id=workoutid)
    deleteworkout.delete()
    return redirect("/dashboard")

def weight_destroy(request, weightid):
    if "user_id" not in request.session:
        return redirect("/")
    deleteweight = Weight.objects.get(id=weightid)
    deleteweight.delete()
    return redirect("/dashboard")

def login(request):

    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0: 
        for key, value in errors.items():
            messages.error(request, value)
        return redirect("/")
    else:
        user = User.objects.filter(email=request.POST['Email']) 
        user = user[0]
        if bcrypt.checkpw(request.POST['Password'].encode(), user.password.encode()):
            request.session["user_id"] = user.id
            return redirect("/dashboard")
        else:
            return redirect("/")

def logout(request):
    if "user_id" not in request.session:
        return redirect("/")
    request.session.clear()
    return redirect("/")