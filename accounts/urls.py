from django.urls import path
from .views import login_view,ChangePasswordView

urlpatterns = [
    path('login/',login_view),
    path('employee/change-password/',ChangePasswordView.as_view(),name="change-password"),
]