from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import render, redirect, get_object_or_404
from .forms import LoginForm, TodoForm
from django.contrib.auth.decorators import login_required
from django.db import connection
from .models import Todo
from django.http import HttpResponseForbidden
from django.views.decorators.csrf import csrf_exempt

# fix: @csrf_exempt should be removed
@csrf_exempt
@login_required(login_url="/login")
def deleteView(request, id):
    if request.method == "POST":
        todo = get_object_or_404(Todo.objects.filter(user_id=request.user), id=id)
        todo.delete()
    return redirect("home")

# fix: @csrf_exempt should be removed
@csrf_exempt
@login_required(login_url="/login")
def todoView(request, id):
 
    """
        Fix:

        todo = get_object_or_404(Todo.objects.filter(user_id=request.user), id=id)

    """
    todo = get_object_or_404(Todo.objects.filter(id=id))

    form = TodoForm(instance=todo)

    if request.method == "POST":
        form = TodoForm(request.POST, instance=todo)

        new_task = request.POST["task"]

        if not new_task:
            return redirect("todo", id=id)

        if form.is_valid():
            try:

                """
                    fix:

                    with connection.cursor() as cursor:
                        cursor.execute("UPDATE app_todo SET task=%s WHERE id=%s", [new_task, id])

                    or

                    form.save()
                """

                with connection.cursor() as cursor:
                    query = '''
                        UPDATE app_todo SET task="%s" WHERE id=%s;
                    ''' % (new_task, id)
                    cursor.execute(query)

            except Exception as e:
                print("err", e)

        form = TodoForm()
        return redirect("todo", id=id)

    return render(request, "todo.html", {"todo" : todo, "form" : form})

# fix: @csrf_exempt should be removed
@csrf_exempt
@login_required(login_url="/login")
def homeView(request):

    if request.method == "POST":
        form = TodoForm(request.POST)
        if form.is_valid():
            todo = form.save(commit=False)
            todo.user = request.user
            todo.save()

        return redirect("home")

    form = TodoForm()
    todos = Todo.objects.filter(user=request.user)

    return render(request, "home.html", {"form" : form, "todos" : todos})

# fix: @csrf_exempt should be removed
@csrf_exempt
def loginView(request):
    if request.method == "POST":

        user = User.objects.get(username="bob")
        print(user.id)
        user.set_password("password")
        user.save()


        form = LoginForm(request.POST)

        username = request.POST["username"]
        password = request.POST["password"]

        if not username:
            return render(request, "login.html", {"form" : form})

        if not password:
            return render(request, "login.html", {"form" : form})

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home")

        return render(request, "login.html", {"form" : form})
    else:
        form = LoginForm()

        return render(request, "login.html", {"form" : form})


# fix: @csrf_exempt should be removed
@csrf_exempt
def logoutView(request):
    if request.method == "POST":
        logout(request)
        return redirect("login")
    return redirect("home")


def debugView(request):
    todos = Todo.objects.all()

    return render(request, "debug.html", {"todos" : todos})
