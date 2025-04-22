from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import Task
from django.contrib import messages
from tracker.models import CustomUser# Import your CustomUser model
from django.db.models import Sum
from tracker import models

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            return redirect('task_list')
        else:
            messages.error(request, 'Invalid credentials.')
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('login')

@login_required
def task_list(request):
    user = request.user
    if user.role == 'manager':
        tasks = Task.objects.all()  # Manager sees all tasks
    else:
        tasks = Task.objects.filter(user=user)  # Employee sees their own
    return render(request, 'task_list.html', {'tasks': tasks})


@login_required
def task_create(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        hours_spent = request.POST['hours_spent']
        tags = request.POST['tags']
        date = request.POST['date']

        # Get the employee assigned to the task (if manager is creating the task)
        employee_id = request.POST.get('employee')
        employee = CustomUser.objects.get(id=employee_id) if employee_id else None

        try:
            # Create the task (validation is handled in the model)
            Task.objects.create(
                user=employee if employee else request.user,  # Assign the task to the employee if manager is creating
                title=title,
                description=description,
                hours_spent=hours_spent,
                tags=tags,
                date=date
            )
            return redirect('task_list')
        except ValueError as e:
            messages.error(request, str(e))

    # Get employees for the manager
    employees = CustomUser.objects.filter(role='employee')  # Use CustomUser here instead of User

    return render(request, 'task_create.html', {'employees': employees})

@login_required
def task_edit(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)
    
    # Check if the task is approved and prevent editing
    if task.status == 'approved':
        messages.error(request, 'Approved tasks cannot be edited.')
        return redirect('task_list')

    if request.method == 'POST':
        # Fetch data from POST request and update task
        task.title = request.POST['title']
        task.description = request.POST['description']
        task.hours_spent = request.POST['hours_spent']  # Ensure the input is in decimal format
        task.tags = request.POST['tags']
        task.date = request.POST['date']
        task.save()
        
        # messages.success(request, 'Task updated successfully!')
        return redirect('task_list')
    
    # Render task edit form
    return render(request, 'task_edit.html', {'task': task})

@login_required
def task_delete(request, id):
    task = get_object_or_404(Task, id=id, user=request.user)  # Only allow the task's owner to delete it
    
    # Check if the task is approved and prevent deletion
    if task.status == 'approved':
        messages.error(request, 'Approved tasks cannot be deleted.')
        return redirect('task_list')
    
    task.delete()  # Delete the task from the database
    messages.success(request, 'Task deleted successfully!')
    return redirect('task_list')


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Task

@login_required
def task_approve(request, id):
    if request.user.role != 'manager':
        return redirect('task_list')  # Redirect non-managers if they try to access the page
    
    task = get_object_or_404(Task, id=id)

    # Check if the task is already approved
    if task.status == 'approved':
        messages.error(request, 'This task is already approved.')
        return redirect('task_list')

    # Update task status and save manager's comment
    task.status = 'approved'
    task.manager_comment = request.POST.get('comment', '')  # Capture manager's comment if provided
    task.save()

    # Provide success feedback
    messages.success(request, 'Task approved successfully!')
    return redirect('task_list')


from django.shortcuts import get_object_or_404, redirect
from django.contrib import messages
from .models import Task

@login_required
def task_reject(request, id):
    if request.user.role != 'manager':
        return redirect('task_list')  # Redirect non-managers if they try to access the page
    
    task = get_object_or_404(Task, id=id)

    # Check if the task is already rejected
    if task.status == 'rejected':
        messages.error(request, 'This task has already been rejected.')
        return redirect('task_list')

    # Update task status to rejected and save manager's comment
    task.status = 'rejected'
    task.manager_comment = request.POST.get('comment', '')  # Capture manager's comment if provided
    task.save()

    # Provide success feedback
    messages.success(request, 'Task rejected successfully!')
    return redirect('task_list')

