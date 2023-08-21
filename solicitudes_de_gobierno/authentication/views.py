from django.shortcuts import render
from django.contrib.auth import authenticate, login

# Create your views here.
def loginView(request):
    if request.method == 'POST':
        email = request.POST['username']
        contrasena = request.POST['password']
        user = authenticate(request, username=email, password=contrasena)

        if user is not None:
            login(request, user)
            # return redirect('dashboard')

        else:
            # Invalid credentials
            error_message = "Invalid username or password."
            return render(request, 'login.html', {'error_message': error_message})

    if request.method == 'GET':
        return render (request, 'login.html')

