from openai import OpenAI
from django.conf import settings

from rest_framework.permissions import IsAuthenticated
from rest_framework import status
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from .models import Meal, MealItem, FoodImage
from .serializers import MealSerializer, FoodImageSerializer
import json
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
import os
import shutil
from member.models import UserProfile
from AiModel import foodClassification,foodRecommendation
import re
from datetime import datetime, timedelta
from django.http import JsonResponse

# Configure OpenAI API
client = OpenAI(api_key=settings.OPENAI_API_KEY)
path = "/Users/parkjihyeon/Desktop/IndonesiaWeb/AiModel/images/"

@api_view(['POST'])
@permission_classes([AllowAny])
def upload_image(request):
    if 'image' not in request.FILES:
        return Response({"error": "No image uploaded"}, status=status.HTTP_400_BAD_REQUEST)

    image = request.FILES['image']
    
    # 경로가 없으면 생성
    if not os.path.exists(path):
        os.makedirs(path)
    
    file_path = os.path.join(path, image.name)
    with open(file_path, 'wb') as f:
        for chunk in image.chunks():
            f.write(chunk)
    
    file_url = f'file://{file_path}'

    return Response({"image_url": file_url}, status=status.HTTP_201_CREATED)


@api_view(['GET'])
@permission_classes([AllowAny])
def meal_list(request):
    try:
        # email과 date를 쿼리 파라미터로 추출
        data = json.loads(request.body)
        email = data.get('email')
        date_str = data.get('date')

        if not email or not date_str:
            return JsonResponse({"error": "Email and date parameters are required"}, status=status.HTTP_400_BAD_REQUEST)

        try:
            member = UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return JsonResponse({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

        try:
            date = datetime.strptime(date_str, "%Y-%m")
        except ValueError:
            return JsonResponse({"error": "Invalid date format. Use YYYY-MM"}, status=status.HTTP_400_BAD_REQUEST)

        start_date = date.replace(day=1)
        end_date = (start_date + timedelta(days=31)).replace(day=1) - timedelta(days=1)

        meals = Meal.objects.filter(email=email, date__range=[start_date, end_date])
        meal_items = MealItem.objects.filter(meal__in=meals)

        # 일별로 데이터를 묶기 위한 딕셔너리
        daily_meals = {}
        for meal in meals:
            meal_date = meal.date.strftime('%Y-%m-%d')
            if meal_date not in daily_meals:
                daily_meals[meal_date] = {
                    "meal_time": meal.meal_time,
                    "items": []
                }

            items = meal_items.filter(meal=meal)
            daily_meals[meal_date]["items"].extend([
                {
                    "id": item.id,
                    "food_name": item.food_name,
                    "calories": item.calories,
                    "carbs": item.carbs,
                    "protein": item.protein,
                    "fat": item.fat
                } for item in items
            ])

        # 칼로리 섭취량 계산
        def calculate_intake_total(items):
            total_calories = sum(int(item['calories'].replace(' kcal', '')) for item in items if item['calories'].replace(' kcal', '').isdigit())
            if member.gender == 'male':
                bmr = 66.47 + (13.75 * member.weight) + (5 * member.height) - (6.76 * member.age)
            else:
                bmr = 655.1 + (9.56 * member.weight) + (1.85 * member.height) - (4.68 * member.age)

            # 간단한 예시: 하루 칼로리 필요량은 BMR
            if total_calories == bmr:
                return "적정량 섭취"
            elif total_calories > bmr:
                return "섭취 초과"
            else:
                return "적정량 부족"

        # 결과 데이터 준비
        result_data = []
        for date, meal_data in daily_meals.items():
            intake_total = calculate_intake_total(meal_data["items"])
            result_data.append({
                "date": date,
                "items": meal_data["items"],
                "intakeTotal": intake_total
            })

        return JsonResponse(result_data, safe=False, status=status.HTTP_200_OK)

    except json.JSONDecodeError:
        return JsonResponse({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    except KeyError:
        return JsonResponse({"error": "Invalid request format"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return JsonResponse({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    


@api_view(['POST'])
@permission_classes([AllowAny])
def meal_item_detail(request):
    try:
        data = json.loads(request.body)
        item_id = data.get('item_id')
        meal_time = data.get('meal_time')

        if not item_id:
            return Response({"error": "item_id parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        if not meal_time:
            return Response({"error": "meal_time parameter is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        # 유효한 meal_time 값인지 확인
        valid_meal_times = dict(Meal.MEAL_CHOICES).keys()
        if meal_time not in valid_meal_times:
            return Response({"error": "Invalid meal_time value"}, status=status.HTTP_400_BAD_REQUEST)

        # MealItem과 연결된 Meal을 조회
        try:
            meal_item = MealItem.objects.get(id=item_id)
            meal = meal_item.meal
            
            if meal.meal_time != meal_time:
                return Response({"error": "Meal item does not match the provided meal_time"}, status=status.HTTP_400_BAD_REQUEST)

            meal_item_data = {
                "id": meal_item.id,
                "food_name": meal_item.food_name,
                "calories": meal_item.calories,
                "carbs": meal_item.carbs,
                "protein": meal_item.protein,
                "fat": meal_item.fat,
                "meal": {
                    "meal_time": meal.meal_time,
                    "date": meal.date
                }
            }
            return Response(meal_item_data, status=status.HTTP_200_OK)
        except MealItem.DoesNotExist:
            return Response({"error": "MealItem not found"}, status=status.HTTP_404_NOT_FOUND)
    except json.JSONDecodeError:
        return Response({"error": "Invalid JSON"}, status=status.HTTP_400_BAD_REQUEST)
    except Exception as e:
        return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    



# 기능: 업로드된 이미지를 기반으로 유사한 음식 이미지를 생성
@api_view(['POST'])
#@permission_classes([IsAuthenticated])
@permission_classes([AllowAny])
def generate_similar_foods(request):

    image = request.FILES['image']

    # 경로가 없으면 생성
    if not os.path.exists(path):
        os.makedirs(path)
    
    file_path = os.path.join(path, image.name)
    with open(file_path, 'wb') as f:
        for chunk in image.chunks():
            f.write(chunk)
    
    file_url = f'file://{file_path}'

    foodClassificationResponse = foodClassification.foodClassification()

    food_names_str = ', '.join(foodClassificationResponse)
    
    recommend_foodResponse = foodRecommendation.recommend_food(food_names_str)
    print(recommend_foodResponse)
    match = re.search(r'"food_name":"(.*?)"', recommend_foodResponse)
    food_name=""
    
    if match:
        food_name = match.group(1)
        print(food_name)
    else:
        print("food_name not found")

    reason_match = re.search(r'"reason":"(.*?)"', recommend_foodResponse, re.DOTALL)

    reason=""  
    if reason_match:
        reason = reason_match.group(1)
        print(reason)
    else:
        print("reason not found")        


    response = foodRecommendation.generate_image(food_name)
    image_url = response.data[0].url


    # 모든 이미지 파일 삭제
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')
        
    return Response({"image_url": image_url,"reason" :reason}, status=status.HTTP_200_OK)


# 기능: 업로드된 이미지에서 식사 정보를 추출하고 저장
@api_view(['POST'])
@permission_classes([AllowAny])
def extract_and_save_meal_info(request):

    image = request.FILES['image']
    email = request.data.get('email')
    meal_time = request.data.get('meal_time')
    meal_date = datetime.now()  # 서버 시간을 식사 날짜로 설정


    # 경로가 없으면 생성
    if not os.path.exists(path):
        os.makedirs(path)
    
    file_path = os.path.join(path, image.name)
    with open(file_path, 'wb') as f:
        for chunk in image.chunks():
            f.write(chunk)
    
    file_url = f'file://{file_path}'

    foodClassificationResponse = foodClassification.foodClassification()
    food_names_str = ', '.join(foodClassificationResponse)
    # 영양 정보 함수 호출
    nutritionResponse = foodRecommendation.nutrition(food_names_str)
    
    nutrition_info = json.loads(nutritionResponse)
    
    print(nutrition_info)

    # 각 정보를 변수에 저장
    food_name = nutrition_info.get('food_name')
    calories = nutrition_info.get('calories')
    carbs = nutrition_info.get('carbohydrates')
    protein = nutrition_info.get('protein')
    fat = nutrition_info.get('fat')


    email = request.data.get('email')  # Get email from request data
    if not UserProfile.objects.filter(email=email).exists():
        return Response({"error": "Member not found"}, status=status.HTTP_404_NOT_FOUND)

    # Save meal information
    meal = Meal.objects.create(
        meal_time=meal_time,
        date=meal_date,
        email=email  # Save with email
    )

    MealItem.objects.create(
        meal=meal,
        food_name=food_name,
        calories=calories,
        carbs=carbs,
        protein=protein,
        fat=fat
    )
    
    # 모든 이미지 파일 삭제
    for filename in os.listdir(path):
        file_path = os.path.join(path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f'Failed to delete {file_path}. Reason: {e}')

    return Response({
        'food_name': food_name,
        'meal_time': meal_time,
        'calories': calories,
        'carbs': carbs,
        'protein': protein,
        'fat': fat
    }, status=status.HTTP_201_CREATED)