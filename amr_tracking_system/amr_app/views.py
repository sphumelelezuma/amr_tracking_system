from django.shortcuts import render, redirect  # Added redirect to handle post-login redirection
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from rest_framework import generics, permissions
from .serializers import PathogenSerializer, LocationSerializer, ResistanceDataSerializer, UserSerializer
from .models import Pathogen, Location, ResistanceData, Post, Comment, Reaction
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from django.contrib.auth import views as auth_views
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm  # Import the built-in form for registration
from .models import Post
from .forms import PostForm
from .forms import ProfilePictureForm
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect
from .models import UserProfile
from .forms import ProfilePictureForm  # Adjust to your actual form
from .forms import ResistanceDataForm
import plotly.express as px
import pandas as pd
import json
from django.http import JsonResponse, HttpResponseNotAllowed, HttpResponseForbidden
from .forms import PathogenForm, LocationForm
from django.db.models import Avg 
from rest_framework.decorators import api_view
from rest_framework.response import Response 
from django.views.decorators.csrf import csrf_exempt
from django.middleware.csrf import get_token

@csrf_exempt  # Only needed if you’re not using the CSRF token
def delete_resistance_data(request, data_id):
    if request.method == 'POST':
        resistance_data = get_object_or_404(ResistanceData, id=data_id)
        resistance_data.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)

def api_visualization_data(request):
    # Query the data
    resistance_data = ResistanceData.objects.all()

    # Extract data for the charts
    locations = list(resistance_data.values_list('location__name', flat=True).distinct())
    resistance_percentages = list(resistance_data.values_list('resistance_percentage', flat=True))
    pathogen_names = list(resistance_data.values_list('pathogen__name', flat=True).distinct())
    pathogen_resistances = list(resistance_data.values_list('resistance_percentage', flat=True))

    # Create a dictionary to hold the data
    data = {
        'resistance_labels': locations,
        'resistance_data': resistance_percentages,
        'pathogen_labels': pathogen_names,
        'pathogen_data': pathogen_resistances
    }

    return JsonResponse(data)

@login_required
def submit_data(request):
    if request.method == 'POST':
        resistance_form = ResistanceDataForm(request.POST)
        if resistance_form.is_valid():
            resistance_data = resistance_form.save(commit=False)
            resistance_data.user = request.user  # Assign the currently logged-in user
            resistance_data.save()
            return redirect('data_review')
    else:
        resistance_form = ResistanceDataForm()

    context = {
        'resistance_form': resistance_form,
        'pathogens': Pathogen.objects.all(),
        'locations': Location.objects.all(),
    }
    return render(request, 'data_entry_form.html', context)

def add_pathogen(request):
    if request.method == 'POST':
        form = PathogenForm(request.POST)
        if form.is_valid():
            pathogen = form.save()
            return JsonResponse({'id': pathogen.id, 'name': pathogen.name})
    return JsonResponse({'error': 'Invalid form data'}, status=400)

def add_location(request):
    if request.method == 'POST':
        form = LocationForm(request.POST)
        if form.is_valid():
            location = form.save()
            return JsonResponse({'id': location.id, 'name': location.name})
    return JsonResponse({'error': 'Invalid form data'}, status=400)

def custom_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            if hasattr(user, 'userprofile'):
                login(request, user)
                return redirect('/admin/')
            else:
                # Handle missing profile case
                return render(request, 'login.html', {'error': 'User has no profile'})
        else:
            # Handle authentication failure
            return render(request, 'login.html', {'error': 'Invalid credentials'})
    return render(request, 'login.html')

def reports(request):
    return render(request, 'reports.html')

def settings(request):
    return render(request, 'settings.html')

def create_profile(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST)
        if form.is_valid():
            # Handle form processing here
            form.save()
            return redirect('profile')  # Redirect to the profile page or wherever you need
    else:
        form = ProfilePictureForm()
    return render(request, 'create_profile.html', {'form': form})


@login_required
def update_profile_picture(request):
    if request.method == 'POST':
        form = ProfilePictureForm(request.POST, request.FILES, instance=request.user.userprofile)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Or the appropriate redirect URL
    else:
        form = ProfilePictureForm(instance=request.user.userprofile)
    
    return render(request, 'update_profile_picture.html', {'form': form})


def workspace(request):
    return render(request, 'workspace.html')

def chat(request):
    return render(request, 'chat.html')

def tasks(request):
    return render(request, 'tasks.html')

def search(request):
    return render(request, 'search.html')

@login_required
def data_entry(request):
    if request.method == 'POST':
        form = ResistanceDataForm(request.POST)
        if form.is_valid():
            pathogen_id = request.POST.get('pathogen')
            if not Pathogen.objects.filter(id=pathogen_id).exists():
                new_pathogen = request.POST.get('new_pathogen')
                if new_pathogen:
                    pathogen = Pathogen.objects.create(name=new_pathogen)
                else:
                    pathogen = Pathogen.objects.get(id=pathogen_id)
            
            location_id = request.POST.get('location')
            if not Location.objects.filter(id=location_id).exists():
                new_location = request.POST.get('new_location')
                if new_location:
                    location = Location.objects.create(name=new_location)
                else:
                    location = Location.objects.get(id=location_id)

            resistance_data = form.save(commit=False)
            resistance_data.pathogen = pathogen
            resistance_data.location = location
            resistance_data.user = request.user  # Assign the currently logged-in user
            resistance_data.save()
            return redirect('data_review')
    else:
        form = ResistanceDataForm()

    pathogens = Pathogen.objects.all()
    locations = Location.objects.all()
    context = {
        'form': form,
        'pathogens': pathogens,
        'locations': locations,
    }
    return render(request, 'data_entry_form.html', context)

@login_required
def data_review(request):
    print("Loged in user: ", request.user)  # Check console for this output
    resistance_data_list = ResistanceData.objects.filter(user=request.user)  # Display data entered by the logged-in user
    return render(request, 'data_review.html', {'resistance_data': resistance_data_list})

# Visualization Dashboard view
@login_required 
def visualization_dashboard(request):
    # Fetch resistance data by location
    resistance_data = ResistanceData.objects.filter(user=request.user).select_related('pathogen', 'location')

    # Group resistance data by location for chart
    locations = [data.location.name for data in resistance_data]
    resistance_percentages = [float(data.resistance_percentage) for data in resistance_data]

    # Group resistance data by pathogen and calculate average resistance percentage for each
    pathogen_data = (
        ResistanceData.objects
        .filter(user=request.user) 
        .values('pathogen__name')  # Group by pathogen name
        .annotate(average_resistance=Avg('resistance_percentage'))  # Calculate average resistance
    )

    # Separate pathogen names and their average resistance percentages for the chart
    pathogen_names = [entry['pathogen__name'] for entry in pathogen_data]
    pathogen_resistances = [float(entry['average_resistance']) for entry in pathogen_data]

    # Convert data to JSON for use in JavaScript
    resistance_labels_json = json.dumps(locations)
    resistance_values_json = json.dumps(resistance_percentages)
    pathogen_labels_json = json.dumps(pathogen_names)
    pathogen_values_json = json.dumps(pathogen_resistances)

    # Convert data to JSON
    context = {
        'locations': json.dumps(locations),
        'resistance_percentages': json.dumps(resistance_percentages),
        'pathogen_names': json.dumps(pathogen_names),
        'pathogen_resistances': json.dumps(pathogen_resistances)
    }

    return render(request, 'visualization_dashboard.html', context)

def view_text_file(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if post.document and post.document.name.endswith('.txt'):
        response = HttpResponse(post.document.read(), content_type='text/plain')
        response['Content-Disposition'] = f'inline; filename="{post.document.name}"'
        return response
    return HttpResponse("File not found or not a text file.")

def my_login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')  # Redirect to a success page, replace 'home' with your desired redirect URL
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})  # Return an 'invalid login' error message
    else:
        return render(request, 'login.html')  # Render the login page if it's a GET request

def my_register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()  # Save the new user to the database
            return redirect('login')  # Redirect to the login page after successful registration
    else:
        form = UserCreationForm()
    return render(request, 'register.html', {'form': form})  # Render the registration page

#Home view
@login_required
def home_view(request):
    return render(request, 'home.html')

#Profile view
@login_required
def profile_view(request):
    print("Profile page accessed")
    return render(request, 'profile.html')  # Make sure you have a profile.html template


# Publications view
def publications(request):
    return render(request, 'publications.html')

#get started button view
@login_required
def get_started(request):
    #Redired to the newsfeed page if the user is logged in
    return redirect('newsfeed')

def get_started_redirect(request):
    # Redirect to the login page if the user is not logged in
    if not request.user.is_authenticated:
        return redirect('login')
    return redirect('newsfeed')

@login_required
def newsfeed_view(request):
    posts = Post.objects.all().order_by('-created_at')
    form = PostForm(request.POST or None, request.FILES or None)

    if form.is_valid():
        post = form.save(commit=False)
        post.user = request.user
        post.save()
        return redirect('newsfeed')

    context = {
        'posts': posts,
        'form': form,
    }

    return render(request, 'newsfeed.html', context)

@login_required
def create_post(request):
    if request.method == 'POST':
        content = request.POST.get('content')
        image = request.FILES.get('image')
        document = request.FILES.get('document')  # Add this line to handle document uploads
        post = Post.objects.create(user=request.user, content=content, image=image, document=document)
        return redirect('newsfeed')
    return render(request, 'create_post.html')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )
    return redirect('newsfeed')

@login_required
def add_reaction(request, post_id, reaction_type):
    post = Post.objects.get(id=post_id)
    Reaction.objects.create(user=request.user, post=post, reaction_type=reaction_type)
    return redirect('newsfeed')

@login_required
def add_reaction(request, post_id, reaction_type):
    post = get_object_or_404(Post, id=post_id)
    if reaction_type not in ['like', 'dislike', 'heart']:
        return redirect('newsfeed')  # Redirect to a safe page if the reaction type is invalid
    
    Reaction.objects.update_or_create(
        user=request.user,
        post=post,
        defaults={'reaction_type': reaction_type}
    )

    return redirect('newsfeed')

@login_required
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == 'POST':
        content = request.POST.get('content')
        if content:
            Comment.objects.create(
                user=request.user,
                post=post,
                content=content
            )
    return redirect('newsfeed')

# Delete post view
@login_required
def delete_post(request, post_id):
    # Get the post object based on the post_id
    post = get_object_or_404(Post, id=post_id)
    
    # If it's a POST request (i.e., the delete form is submitted)
    if request.method == 'POST':
        post.delete()  # Delete the post
        return redirect('newsfeed')  # Redirect to the newsfeed or another page after deletion
    

# amr_app/views.py

# ... existing imports and views ...

# API Views for Pathogen
class PathogenListCreateAPIView(generics.ListCreateAPIView):
    queryset = Pathogen.objects.all()
    serializer_class = PathogenSerializer
    permission_classes = [permissions.IsAuthenticated]

class PathogenRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Pathogen.objects.all()
    serializer_class = PathogenSerializer
    permission_classes = [permissions.IsAuthenticated]

# API Views for Location
class LocationListCreateAPIView(generics.ListCreateAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

class LocationRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Location.objects.all()
    serializer_class = LocationSerializer
    permission_classes = [permissions.IsAuthenticated]

# API Views for ResistanceData
class ResistanceDataListCreateAPIView(generics.ListCreateAPIView):
    queryset = ResistanceData.objects.all()
    serializer_class = ResistanceDataSerializer
    permission_classes = [permissions.IsAuthenticated]

class ResistanceDataRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = ResistanceData.objects.all()
    serializer_class = ResistanceDataSerializer
    permission_classes = [permissions.IsAuthenticated]

# User API views should be accessible by admin users only
class UserListCreateAPIView(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Admin users only

class UserRetrieveUpdateDestroyAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAdminUser]  # Admin users only
