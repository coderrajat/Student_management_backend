from django.urls import path
from . import views


urlpatterns = [
    path('student_registration',views.Student_Register.as_view(), name='Registration'),
    path('login_student',views.Student_login_api.as_view(), name='SignIn'),
]