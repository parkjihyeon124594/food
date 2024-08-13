from django.db import models
from member.models import UserProfile

class Meal(models.Model):
    MEAL_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    
    meal_time = models.CharField(max_length=10, choices=MEAL_CHOICES)
    date = models.DateField()
    email = models.EmailField(null=True)  # Email field to store member's email

    def __str__(self):
        return f"{self.email} - {self.meal_time} on {self.date}"

class MealItem(models.Model):
    meal = models.ForeignKey(Meal, related_name='items', on_delete=models.CASCADE)
    food_name = models.CharField(max_length=100)
    calories = models.CharField(max_length=50)
    carbs = models.CharField(max_length=50)
    protein = models.CharField(max_length=50)
    fat = models.CharField(max_length=50)

    def __str__(self):
        return self.food_name

class FoodImage(models.Model):
    image = models.ImageField(upload_to='food_images/')
    member_email = models.EmailField()  # Email field to store member's email
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image {self.id} by {self.member_email}"
