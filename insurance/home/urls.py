from django.urls import path
from home import views

urlpatterns = [
    path('',views.homepage,name='homepage'),
    path('home/',views.index, name = "home"),
    path('about/', views.about, name = "about"),
    path('contact/', views.contact, name = "contact"),
    path('prediction/', views.prediction, name = "prediction"),
    path('heart-disease/', views.heart_disease, name = "heart-disease"),
    path('heart-disease_pred/',views.heart_disease_prediction, name = "heart-disease_pred"),
    path('liver-disease/', views.liver_disease, name = "liver-disease"),
    path('signup/', views.registerPage, name='signup'),
    path('login/', views.loginPage, name='login'),
    path('logout/', views.logout, name='logout'),
    path('chatbot/', views.chatbot, name='chatbot'),
    
]
