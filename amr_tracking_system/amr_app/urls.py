from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from . import views
from .views import (
    add_pathogen,  # Add view for adding pathogens
    add_location,  # Add view for adding locations
    view_text_file,
    home_view,
    profile_view,
    get_started,
    get_started_redirect,
    PathogenListCreateAPIView,
    PathogenRetrieveUpdateDestroyAPIView,
    LocationListCreateAPIView,
    LocationRetrieveUpdateDestroyAPIView,
    ResistanceDataListCreateAPIView,
    ResistanceDataRetrieveUpdateDestroyAPIView,
    UserListCreateAPIView,
    UserRetrieveUpdateDestroyAPIView,
)


urlpatterns = [
    path('login/', views.my_login_view, name='login'),
    path('register/', views.my_register_view, name='register'),  # Add the new registration view
    path('', views.home_view, name='home'),
    path('logout/', auth_views.LogoutView.as_view(next_page='home'), name='logout'),
    path('profile/', views.profile_view, name='profile'),  # Add this line
    path('publications/', views.publications, name='publications'),  # Publications page
    path('password_change/', auth_views.PasswordChangeView.as_view(), name='password_change'),
    path('get-started/', views.get_started_redirect, name='get_started_redirect'),
    path('newsfeed/', views.newsfeed_view, name='newsfeed'),
    path('api/newsfeed/', views.newsfeed_view, name='newsfeed'),
    path('newsfeed/reaction/<int:post_id>/<str:reaction_type>/', views.add_reaction, name='add_reaction'),
    path('newsfeed/comment/<int:post_id>/', views.add_comment, name='add_comment'),
    path('delete_post/<int:post_id>/', views.delete_post, name='delete_post'),
    path('view_text_file/<int:post_id>/', view_text_file, name='view_text_file'),
    path('workspace/', views.workspace, name='workspace'),
    path('chat/', views.chat, name='chat'),
    path('tasks/', views.tasks, name='tasks'),
    path('search/', views.search, name='search'),
    path('data_entry/', views.data_entry, name='data_entry'),
    path('data_review/', views.data_review, name='data_review'),
    path('visualization_dashboard/', views.visualization_dashboard, name='visualization_dashboard'),
    path('update_profile_pic/', views.update_profile_picture, name='update_profile_pic'),
    path('update-profile-picture/', views.update_profile_picture, name='update_profile_picture'),
    path('create-profile/', views.create_profile, name='create_profile'),  
    path('reports/', views.reports, name='reports'),
    path('settings/', views.settings, name='settings'),  
    path('add_pathogen/', views.add_pathogen, name='add_pathogen'),
    path('add_location/', views.add_location, name='add_location'), 
    path('submit-data/', views.submit_data, name='submit_data'),
    # ... existing URL patterns ...

    # API Endpoints
    path('api/pathogens/', PathogenListCreateAPIView.as_view(), name='api_pathogen_list_create'),
    path('api/pathogens/<int:pk>/', PathogenRetrieveUpdateDestroyAPIView.as_view(), name='api_pathogen_detail'),
    
    path('api/locations/', LocationListCreateAPIView.as_view(), name='api_location_list_create'),
    path('api/locations/<int:pk>/', LocationRetrieveUpdateDestroyAPIView.as_view(), name='api_location_detail'),
    
    path('api/resistance-data/', ResistanceDataListCreateAPIView.as_view(), name='api_resistancedata_list_create'),
    path('api/resistance-data/<int:pk>/', ResistanceDataRetrieveUpdateDestroyAPIView.as_view(), name='api_resistancedata_detail'),
    
    path('api/users/', UserListCreateAPIView.as_view(), name='api_user_list_create'),
    path('api/users/<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='api_user_detail'),
]  
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)


