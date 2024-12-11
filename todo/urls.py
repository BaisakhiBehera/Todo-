from django.urls import path
from . import views


urlpatterns = [
    path('', views.signup, name='signup'),
    path('login_page', views.Login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('todo_page',views.todo_list,name='todo'),
    path('todo_get',views.todo_get,name='todo_get'),
    path('todo_delete/<int:id>',views.todo_delete,name='tododel'),
    path('todo_update/<int:id>',views.todo_update,name='todo_update'),
]