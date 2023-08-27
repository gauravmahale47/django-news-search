from django.views import View
from django.contrib import messages
from django.http import HttpResponse
from NewsSearchApp.enum import HttpCodes
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout
from auth_management.forms import RegistrationForm, LoginForm
from django.contrib.auth.decorators import login_required, permission_required


app_name = "auth_management"


class HomePageView(View):
    def get(self, request):
        """
        This method will be called when the user visits the home page.
        It will render the home page.
        """
        return render(request, "auth/index.html")


class RegistrationView(View):
    def get(self, request):
        """
        This method will be called when the user visits the registration page.
        It will render the registration form.
        """

        form = RegistrationForm()
        context = {"form": form}
        return render(request, "auth/registration.html", context=context)

    def post(self, request):
        """
        This method will be called when the user submits the registration form.
        It will validate the form and create a new user.
        """

        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(
                request,
                "Congratulations, your account has been successfully created. Please Login.",
            )
            return redirect("auth_management:login")
        else:
            for field, errors in form.errors.items():
                error_messages = ", ".join(errors)
                messages.error(request, f"Error in {field}: {error_messages}")
        return redirect("auth_management:registration")


class LoginView(View):
    def get(self, request):
        """
        This method will be called when the user visits the login page.
        It will render the login form.
        """

        form = LoginForm()
        context = {"form": form}
        return render(request, "auth/login.html", context=context)

    def post(self, request):
        """
        This method will be called when the user submits the login form.
        It will validate the form and authenticate the user.
        """
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "You have successfully logged in.")
            return redirect("auth_management:home")
        else:
            user = User.objects.filter(username=username).first()
            if user and user.is_active == False:
                messages.error(
                    request,
                    "Invalid username or password or your account is not active. Please contact the administrator.",
                )
            else:
                messages.error(request, "Invalid username.")
        return redirect("auth_management:login")


@method_decorator(login_required(login_url="auth_management:login"), name="dispatch")
class LogOutView(View):
    def get(self, request):
        """
        This method will be called when the user clicks on the logout button.
        It will logout the user.
        """

        logout(request)
        messages.success(request, "You have successfully logged out.")
        return redirect("auth_management:login")


@method_decorator(login_required(login_url="auth_management:login"), name="dispatch")
@method_decorator(permission_required(["auth_management.view_user", "auth_management.add_user"]), name="dispatch")
class AdminCollectionView(View):
    def get(self, request):
        """
        This method will be called when the user visits the admin page.
        It will render the admin page.
        """

        users = User.objects.exclude(id=request.user.id)
        context = {
            "users": users
        }
        return render(request, "auth/admin.html", context=context)

    def post(self, request):
        """
        This method will be called when the admin submits the registration form.
        It will validate the form and create a new user.
        """

        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Congratulations, user successfully created.")
        else:
            for field, errors in form.errors.items():
                error_messages = ", ".join(errors)
                messages.error(request, f"Error in {field}: {error_messages}")
        return redirect("auth_management:admin")
    

@method_decorator(login_required(login_url="auth_management:login"), name="dispatch")
@method_decorator(permission_required(["auth_management.view_user", "auth_management.change_user"]), name="dispatch")
class AdminSingleView(View):
    def put(self, request, pk):
        """
        This method will be called when the admin updates the user.
        It will update the user active status.
        """

        user = User.objects.get(id=pk)
        user.is_active = not user.is_active
        user.save()
        if user.is_active:
            messages.success(request, "User successfully activated.")
        else:
            messages.success(request, "User successfully deactivated.")
        return HttpResponse(status=HttpCodes.HTTP_200_OK.value)