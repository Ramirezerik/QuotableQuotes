from django.urls import path
from . import views

urlpatterns = [
    path('', views.index),               #localhost:8000/
    path('register', views.register),   #localhost:8000/register
    path('login', views.login),         #localhost:8000/login
    path('quotes', views.dashboard),     #localhost:8000/quotes (changed from show_all)
    path("quotes/create", views.create_quote), #localhost:8000/quotes/create
    path("quotes/<int:user_id>", views.users), #localhost:8000/quotes/2 (changed from show_one and int:quote_id)
    path("quotes/<int:quote_id>/update", views.update), #localhost:8000/quotes/2/update
    path("quotes/<int:quote_id>/edit", views.edit), #localhost:8000/quotes/2/edit
    path("quotes/<int:quote_id>/delete", views.delete), #localhost:8000/quotes/2/delete
    path("favorite/<int:quote_id>", views.favorite), #localhost:8000/quotes/2 (changes quote to liked)
    path("unfavorite/<int:quote_id>", views.unfavorite), #localhost:8000/quotes/2 (changes a liked quote to not liked)
    path("logout", views.logout)        #localhost:8000/ (redirects us to login page)
]