from django.urls import path
from . import views
from .views import webcam_stream, webcam_stream2, AccountantPageView, DownloadFileView, SupportRequestView, ProfileView, \
    webcam_stream_add_face

urlpatterns = [
    path("guard", views.GuardView.as_view(), name='kpp'),
    path("login", views.LoginView.as_view(), name='login'),
    path("", views.RedirectView.as_view(), name='redirect'),
    path('logout', views.LogoutView.as_view(), name='logout'),
    path('unknown', views.UnknownView.as_view(), name='unknown'),
    path('watcher', views.WatcherView.as_view(), name='watcher'),
    path('user/all/', views.UsersListView.as_view(), name='user_list'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user_detail'),
    path('user/add/', views.AddUserView.as_view(), name='add_user'),
    path('user/<int:pk>/update/', views.UpdateUserView.as_view(), name='update_user'),
    path('user/<int:pk>/update/', views.UpdateUserView.as_view(), name='delete_user'),
    path('webcam_stream1/', webcam_stream, name='webcam_stream'),
    path('webcam_stream2/', webcam_stream2, name='webcam_stream'),
    path('accountant/', AccountantPageView.as_view(), name='accountant'),
    path('download-file/', DownloadFileView.as_view(), name='download_file'),
    path('submit-support-request/', SupportRequestView.as_view(), name='submit_support_request'),
    path('profile/', ProfileView.as_view(), name='profile'),
    path('register_faces/list/', views.UsersAddFaceListView.as_view(), name='register_faces_list'),
    path('register_faces/<int:pk>/', views.UserAddFaceDetailView.as_view(), name='register_faces'),
]
