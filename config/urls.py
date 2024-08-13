
from django.contrib import admin
from django.conf import settings
from django.urls import path,include
import dietRecommendation.views
import foods.views
from member.views import LoginView, LogoutView, RegisterView, register_view, login_view,post

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/diet-recommendation',dietRecommendation.views.dietRecommenationViews),
    path('api/images/upload',foods.views.upload_image),   
    path('api/meals',foods.views.meal_list),
    path('api/meals/details',foods.views.meal_item_detail),
    path('api/foods/similar',foods.views.generate_similar_foods),
    path('api/meals/extract',foods.views.extract_and_save_meal_info),
    #
    #path('api_login/', LoginView.as_view(), name='api-login'),
    path('api_login/',post),
    path('api_register/', RegisterView.as_view(), name='api-register'),     

    path('', include('foods.urls')),
]
