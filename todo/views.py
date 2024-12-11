from django.shortcuts import render,redirect
from .models import User,Todo
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.http import HttpResponse
import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import get_object_or_404
from django.core.mail import send_mail
# Create your views here.

def signup(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')   
        password = request.POST.get('password')
        # if User.objects.filter(username=email).exists():
        #     return HttpResponse("user with this email already exists, pls try with another email")
        new_user = User.objects.create(first_name=name, username =email)
        new_user.set_password(password)
        new_user.save()
        # user_email = new_user.username
        # data = [user_email]
        # print(new_user.username)
        # subject = 'Welcome to Todo App'
        # message = "create and manage your todos"
        # from_email  = "todo_by_baisakhi"
        # send_mail(subject, message,from_email, data)

        return redirect('login')
    return render(request,'signup.html')

def Login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user:
            login(request, user)
            return render(request, 'home.html')
            return redirect ('todo') 
        
        else:
            #messages.error(request, "Invalid credentials.")
            return HttpResponse("Invalid credentials.")
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    messages.error(request, 'Logged out successfully!')
    return redirect('login')
def todo_list(request):
    
    if request.method == 'POST':
        user_details = request.user
        title = request.POST.get('title')
        description = request.POST.get('description')
        new_todo = Todo.objects.create(title=title, description=description,user=user_details)
        new_todo.save()
        return render(request, 'home.html')

        
        
    return render(request, 'todo.html')

def todo_get(request):
    if request.method == 'GET':
        user = request.user
        todos = Todo.objects.filter(user=user)                  
        todo_data = []
        for todo in todos:
            todo_data.append({
                    'id': todo.id,
                    'title': todo.title,
                    'description': todo.description
                })
        
    # Return the data as JSON response
    #

    return JsonResponse(todo_data, safe=False)

def todo_delete(request,id):
    
    if request.method == 'DELETE':
        data = Todo.objects.get(id=id)
        data.delete()

    return HttpResponse("Deleted Succesfully")


def todo_update(request, id):
    if request.method == 'PUT':
        try:
            
            data = json.loads(request.body)
            new_title = data.get('title') 

            if not new_title:
                return JsonResponse({'error': 'Title is required'}, status=400)

            # Find the todo item by id
            todo = Todo.objects.get(id=id)
            todo.title = new_title  # Update the title
            todo.save()  # Save the changes

            return JsonResponse({'message': 'Todo updated successfully'})

        except Todo.DoesNotExist:
            return JsonResponse({'error': 'Todo not found'}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)

    return JsonResponse({'error': 'Invalid request method'}, status=405)