from django.urls import path, include
from account.views import (
    user_registration, 
    activate, 
    log_in, 
    log_out, 
    dashboard,
    reset_user_init_password,
    # profile,
    # update_profile,
    user_profile
    )

urlpatterns = [
    path('', user_registration, name="register"),
    path('login/', log_in, name="login"),
    path('logout/', log_out, name="logout"),
    path('dashboard/', dashboard, name="dashboard"),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('reset_password/<int:id>/', reset_user_init_password, name="reset_password"),
    path('profile', user_profile, name="profile")
    # path('profile/', profile, name="profile"),
    # path('update_profile/', update_profile, name="update_profile"),
]
