from django.db import models
import re
import bcrypt
import datetime

class UserManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        # add keys and values to errors dictionary for each invalid field
        if len(postData["f_name"]) < 2:
            errors["f_name"] = "First name must be 2 characters or greater."
        if len(postData["l_name"]) < 2:
            errors["l_name"] = "Last name must be 2 characters or greater."

        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['Email']):
            errors['Email'] = ("Invalid email address!")
        user = User.objects.filter(email=postData["Email"])
        if user:
            errors["Email"] = "This email is already in use"
        if len(postData["Password"]) < 8:                                  
            errors["Password"] = "Passwords should be at least 8 characters."  
        if postData["Password"] != postData["Verify_Password"]:
            errors["Verify_Password"] = "Passwords must be identical."
        return errors

    def login_validator(self, postData):
        errors = {}
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        if not EMAIL_REGEX.match(postData['Email']):
            errors['Email'] = ("Invalid email address!")
        user = User.objects.filter(email = postData["Email"])
        if user:
            logged_user = user[0]
            if not bcrypt.checkpw(postData["Password"].encode(), logged_user.password.encode()):
                errors["Password"] = "Login information is not valid" 
        if len(postData["Password"]) < 8:                                 
            errors["Password"] = "Incorrect Password." 
        return errors

class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    objects = UserManager()

#######################################################################################################   

class FoodManager(models.Manager):
    def food_validator(self, postData):
        errors = {}
        if len(postData["food"]) < 3:
            errors["food"] = "You need to enter a food to log!"
        try:
            if postData["food_type"] == "":
                errors["food_type"] = "Invalid meal type"
        except:
            errors["food_type"] = "You must choose a Type of Meal"
        
        return errors

class Food(models.Model):
    food_item = models.TextField()
    meal_type = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="foods", on_delete = models.CASCADE)
    objects = FoodManager()

#######################################################################################################

class WorkoutManager(models.Manager):
    def workout_validator(self, postData):
        errors = {}
        if len(postData["workout"]) < 3:
            errors["workout"] = "You need to enter a Workout."
        try:
            if postData["type"] == "":
                errors["type"] = "Invalid type of Workout"
        except:
            errors["type"] = "You must choose a type of Workout"
        if len(postData["time"]) < 1:
            errors["time"] = "Time should be 10 minutes or greater."
        return errors

class Workout(models.Model):
    workout_type = models.TextField()
    time = models.CharField(max_length=3)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WorkoutManager()
    user = models.ForeignKey(User, related_name="workouts", on_delete = models.CASCADE)

#########################################################################################################

class WeightManager(models.Manager):
    def weight_validator(self, postData):
        errors = {}
        if len(postData["weight"]) < 4:
            errors["weight"] = "Weight should be in number form ex: 165.5."
        return errors

class Weight(models.Model):
    weight = models.DecimalField(max_digits=4, decimal_places=1)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = WeightManager()
    user = models.ForeignKey(User, related_name="weights", on_delete = models.CASCADE)