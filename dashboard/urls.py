from django.urls import path
from dashboard.views import( 
    dashboard,
    create_news, 
    reset_user_init_password,
    show_user_profile_data,
    update_user_profile,
)

urlpatterns = [
    path('news-form/', create_news, name="news-form"), 
    path('dashboard/', dashboard, name="dashboard"),
    path('reset_password/', reset_user_init_password, name="reset_password"),
    path('profile/', show_user_profile_data, name="show_profile"),
    path('update_profile/', update_user_profile, name="update_profile"),
]
