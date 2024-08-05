from django import forms

class PostForm(forms.Form):
    COUNTRY_CHOICES = [
        ('ID', 'Indonesia'),
        ('KR', 'Korea'),
    ]
    
    MEAL_TIME_CHOICES = [
        ('breakfast', 'Breakfast'),
        ('lunch', 'Lunch'),
        ('dinner', 'Dinner'),
    ]
    
    country = forms.ChoiceField(choices=COUNTRY_CHOICES)
    meal_time = forms.ChoiceField(choices=MEAL_TIME_CHOICES)
    email = forms.EmailField()
