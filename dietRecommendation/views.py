from openai import OpenAI
from django.conf import settings

from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from datetime import timedelta
import json
from .forms import PostForm
from member.models import Member
from rest_framework.permissions import AllowAny

from foods.models import Meal, MealItem, FoodImage
from foods.serializers import MealSerializer, FoodImageSerializer
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from AiModel import foodClassification
from AiModel import dietRecommendation

# Configure OpenAI API
client = OpenAI(api_key=settings.OPENAI_API_KEY)
#client =OpenAI(api_key='sk-vW-Pte2WN_hlhm__LbfjyXCVAfmsWzgzHkxia5FT47T3BlbkFJyl9ythf6RhiIawVER8gb3AHQMDDC8ob_n6R4KFIMEA')

@api_view(['POST'])
@permission_classes([AllowAny])
def dietRecommenationViews(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            form = PostForm(data)

            if form.is_valid():
                country = form.cleaned_data['country']
                meal_time = form.cleaned_data['meal_time']
                email = form.cleaned_data['email']

                # 멤버 정보 검색
                try:
                    member = Member.objects.get(email=email) # 
                    member_info = {
                        'age': member.age,
                        'height': member.height,
                        'medical_history': member.medical_history,
                        'gender': member.gender,
                        'weight': member.weight,
                    }
                except Member.DoesNotExist:
                    member_info = None

                # 현재 시간과 1달 전 시간 계산
                now = timezone.now()
                one_month_ago = now - timedelta(days=30)

                # foods_meal에서 최근 1달 동안의 식사 ID 가져오기
                recent_meal_ids = Meal.objects.filter(
                    email=email,
                    date__gte=one_month_ago
                ).values_list('id', flat=True)

                # foods_mealitem에서 해당 ID로 food_name 리스트 가져오기
                food_names = MealItem.objects.filter(
                    meal_id__in=recent_meal_ids
                ).values_list('food_name', flat=True)

                food_names_str = ', '.join(food_names)
                
                
                response_data = dietRecommendation.recommend_diet(country,meal_time,member_info,food_names_str)
                response_dict = json.loads(response_data)
                
                #return response_data
                return JsonResponse(response_dict, status=200,safe=False)
            else:
                return JsonResponse({'error': 'Invalid data', 'details': form.errors}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    return JsonResponse({'error': 'Invalid request method'}, status=405)