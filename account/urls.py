from django.urls import path, include
from account.views import (
    user_registration, 
    activate, 
    log_in, 
    log_out, 
    home,
    deactivate_account,
    )

urlpatterns = [
    path('', home, name="home"),
    path('register/', user_registration, name="register"),
    path('login/', log_in, name="login"),
    path('logout/', log_out, name="logout"),
    path('activate/<uidb64>/<token>', activate, name='activate'),
    path('deactivate_account/', deactivate_account, name="deactivate_account"),

]
