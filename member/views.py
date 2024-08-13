from django.contrib.auth.hashers import check_password
from django.http import Http404, JsonResponse
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth import get_user_model
from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from rest_framework import generics
from .serializers import RegisterSerializer
from .models import UserProfile
from django.contrib.auth.backends import BaseBackend
from django.contrib.auth import get_user_model
import json
from django.http import JsonResponse

User = get_user_model()

# Register: Create User
class RegisterView(generics.CreateAPIView):
    
    queryset =UserProfile.objects.all()
    serializer_class = RegisterSerializer
    permission_classes = [permissions.AllowAny]
    
    def post(self, request, *args, **kwargs):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return JsonResponse({'message': 'User created successfully'}, status=status.HTTP_201_CREATED)
        return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

def register_view(request):
    if request.method == 'POST':
        form_data = {
            'username': request.POST.get('username'),
            'email': request.POST.get('email'),
            'password': request.POST.get('password'),
            'full_name': request.POST.get('full_name'),
            'profile_picture': request.FILES.get('profile_picture'),  # Handle file upload
            'phone_number': request.POST.get('phone_number'),
            'date_of_birth': request.POST.get('date_of_birth'),
            'gender': request.POST.get('gender'),
            'height': request.POST.get('height'),
            'weight': request.POST.get('weight'),
            'medical_history': request.POST.get('medical_history')
        }

        serializer = RegisterSerializer(data=form_data)
        if serializer.is_valid():
            serializer.save()
            return redirect('login.html')  # Redirect to a success page or login page
        else:
            # Handle validation errors
            return JsonResponse(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    else:
        return render(request, 'register.html') 

# Login 
def post(request):
    data = json.loads(request.body)
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return JsonResponse({"message": "Email and password are required"}, status=400)

    try:
        user =UserProfile.objects.get(email=email)
    except UserProfile.DoesNotExist:
        return JsonResponse({"message": "Invalid credentials"}, status=400)

    if check_password(password, user.password):
            # Password matches, login successful
        response = JsonResponse({"message": "Login successful"}, status=200)
        response.set_cookie('user_email', email, max_age=3600)  # Cookie expires in 1 hour
        return response
    else:
            # Password does not match
        return JsonResponse({"message": "Invalid credentials"}, status=400)

''' class LoginView(APIView):
    def post(self, request):
        email = request.data.get('email')
        password = request.data.get('password')
    

        if not email or not password:
            return JsonResponse({"message": "Email and password are required"}, status=400)

        try:
            user =UserProfile.objects.get(email=email)
        except UserProfile.DoesNotExist:
            return JsonResponse({"message": "Invalid credentials"}, status=400)

        if check_password(password, user.password):
            # Password matches, login successful
            response = JsonResponse({"message": "Login successful"}, status=200)
            response.set_cookie('user_email', email, max_age=3600)  # Cookie expires in 1 hour
            return response
        else:
            # Password does not match
            return JsonResponse({"message": "Invalid credentials"}, status=400)
        
'''

def login_view(request):
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')
        user = authenticate(request, email=email, password=password)
        if user is not None:
            auth_login(request, user)
            return redirect('home.html')  # Redirect to a success page
        else:
            return JsonResponse({'error': 'Invalid email or password'}, status=status.HTTP_400_BAD_REQUEST)
    else:
        return render(request, 'login.html')

# Logout
class LogoutView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        logout(request)
        return Response({"message": "Logout successful"}, status=status.HTTP_200_OK)
    

''' 
# Update User Data (Register1 Fields)
class UpdateUserView(generics.UpdateAPIView):
    queryset = MemberProfile.objects.all()
    serializer_class = UpdateUserSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        return self.request.user

# Update Member Profile Data (Register2 Fields)
class UpdateProfileView(generics.UpdateAPIView):
    queryset = MemberProfile.objects.all()
    serializer_class = UpdateProfileSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_object(self):
        try:
            return MemberProfile.objects.get(user=self.request.user)
        except MemberProfile.DoesNotExist:
            raise Http404("Profile not found")
            '''