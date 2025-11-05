from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .models import NormalUser, Article, STATUS_UNDER_REVIEW, STATUS_ACCEPTED, STATUS_REJECTED
from .forms import CustomUserForm, UserRegisterForm, PaperUploadForm
from django.contrib.auth.models import Group
from apps.permissions.models import CustomUser

@login_required
def update_profile(request):
    # Get or create the NormalUser profile
    try:
        user_profile = NormalUser.objects.get(normal_user=request.user)
    except NormalUser.DoesNotExist:
        # Create new profile with user data
        user_profile = NormalUser(
            normal_user=request.user,
            full_name=f"{request.user.first_name} {request.user.last_name}".strip() or request.user.username,
            email=request.user.email
        )
        user_profile.save()

    if request.method == 'POST':
        # Basic Info
        user_profile.full_name = request.POST.get('full_name', '')
        user_profile.email = request.POST.get('email', '')
        user_profile.contact = request.POST.get('phone', '')
        user_profile.address = request.POST.get('address', '')
        
        # Academic Info
        user_profile.institution = request.POST.get('institution', '')
        user_profile.department = request.POST.get('department', '')
        user_profile.bio = request.POST.get('bio', '')
        user_profile.research_interests = request.POST.get('research_interests', '')
        user_profile.gender = request.POST.get('gender', 'Male')
        
        # Social Links
        user_profile.website = request.POST.get('website', '')
        user_profile.linkedin = request.POST.get('linkedin', '')
        user_profile.google_scholar = request.POST.get('google_scholar', '')
        user_profile.researchgate = request.POST.get('researchgate', '')

        # Profile Image
        if request.FILES.get('profile_image'):
            user_profile.image = request.FILES['profile_image']

        try:
            user_profile.save()
            messages.success(request, 'Profile updated successfully!')
        except Exception as e:
            messages.error(request, f'Error updating profile: {str(e)}')
        
        return redirect('user:update_profile')

    context = {
        'title': 'Profile Settings',
        'user_profile': user_profile,
        'article_count': Article.objects.filter(user=request.user).count(),
        'review_count': Article.objects.filter(user=request.user, status=STATUS_UNDER_REVIEW).count(),
        'accepted_count': Article.objects.filter(user=request.user, status=STATUS_ACCEPTED).count()
    }
    
    return render(request, 'user/profile_settings.html', context)

def user_register(request):
    auth_form = CustomUserForm()
    user_form = UserRegisterForm()
    context = {
        'title':'Register',
        'auth_form':auth_form,
        'user_form':user_form
    }
    if request.method == 'POST':
        auth_form = CustomUserForm(request.POST,request.FILES)
        user_form = UserRegisterForm(request.POST,request.FILES)
        
        if auth_form.is_valid() and user_form.is_valid():
            username = auth_form.cleaned_data["username"]
            password1 = auth_form.cleaned_data["password1"]
            password2 = auth_form.cleaned_data["password2"]
            
            if request.FILES.get('image'):
                image_url = request.FILES['image']
            else:
                image_url = None
           
            group = Group.objects.get(name = 'User')
            
            if password1 == password2:
                try:
                    # Create the user
                    user = CustomUser.objects.create_user(
                        username=username, 
                        password=password2,
                        user_type=group
                    )
                    # Add user to User group
                    user.groups.clear()  # Clear any existing groups
                    user.groups.add(group)
                    user.save()
                    
                    print(f"User created: {user.username}")
                    print(f"User groups: {list(user.groups.all())}")
                    
                    # Create or get the NormalUser profile
                    normal_user, created = NormalUser.objects.get_or_create(
                        normal_user=user,
                        defaults={
                            'full_name': user_form.cleaned_data['full_name'],
                            'email': user_form.cleaned_data['email']
                        }
                    )
                    
                    # Update profile fields
                    normal_user.full_name = user_form.cleaned_data['full_name']
                    normal_user.email = user_form.cleaned_data['email']
                    normal_user.dob = user_form.cleaned_data.get('dob')
                    normal_user.gender = user_form.cleaned_data.get('gender', 'Male')
                    normal_user.contact = user_form.cleaned_data.get('contact', '')
                    normal_user.address = user_form.cleaned_data.get('address', '')
                    
                    if image_url:
                        normal_user.image = image_url
                    
                    normal_user.save()
                    
                    messages.success(request, "Successfully created your account! Please login.")
                    return redirect('login')
                    
                except Group.DoesNotExist:
                    messages.error(request, "User group does not exist. Please contact administrator.")
                except Exception as e:
                    messages.error(request, f"Error creating account: {str(e)}")
            else:
                messages.error(request, 'Passwords do not match. Please check it properly.')
        
    return render(request,'users/registers.html',context)

from apps.admin_user.models import Category

def upload_article(request):
    # Get all available categories
    categories = Category.objects.all()
    
    if request.method == 'POST':
        form = PaperUploadForm(request.POST, request.FILES)
        if form.is_valid():
            article = form.save(commit=False)
            article.user = request.user
            article.status = STATUS_UNDER_REVIEW
            
            # Handle category
            category_id = request.POST.get('category')
            if category_id:
                try:
                    category = Category.objects.get(id=category_id)
                    article.category = category
                except Category.DoesNotExist:
                    messages.error(request, "Selected category does not exist.")
                    return redirect('user:upload-article')
            
            article.save()
            messages.success(request, "Manuscript submitted successfully! Your submission is now under review.")
            return redirect('user:track-submissions')
        else:
            messages.error(request, "Please correct the errors below.")
    else:
        form = PaperUploadForm()
    
    context = {
        'title': 'Submit Manuscript',
        'form': form,
        'categories': categories
    }
    return render(request, 'users/paper_upload_v2.html', context)

def track_submissions(request):
    articles = Article.objects.filter(user=request.user).order_by('-created_at')
    context = {
        'title': 'Track Submissions',
        'articles': articles
    }
    return render(request, 'users/track_submissions.html', context)

def article_under_review(request):
    articles = Article.objects.filter(user=request.user)
    articles_under_review = Article.objects.filter(status=STATUS_UNDER_REVIEW, user=request.user)
    context = {
        'title':'View Paper',
        'articles_under_review':articles_under_review,
    }
    return render(request,'users/article-under-review.html',context)

def accepted_article_list(request):
    articles = Article.objects.filter(user=request.user)
    accepted_articles = Article.objects.filter(status=STATUS_ACCEPTED, user=request.user)
    accepted_feedback = []
    for article in articles:
        article_obj = get_object_or_404(Article, pk=article.pk)
        article_feedback = article_obj.feedback_set.all()
        for feedback in article_feedback:     
            if feedback.status == 'Accepted':
                accepted_feedback.append(feedback)
    
    context = {
        'title':'Accepted Paper',
        'accepted_articles':zip(accepted_articles,accepted_feedback)
    }
    return render(request,'users/accepted_articles.html',context)

def rejected_article_list(request):
    articles = Article.objects.filter(user=request.user)
    rejected_articles = Article.objects.filter(status=STATUS_REJECTED, user=request.user)
    rejected_feedback = []
    for article in articles:
        article_obj = get_object_or_404(Article, pk=article.pk)
        article_feedback = article_obj.feedback_set.all()
        for feedback in article_feedback:     
            if feedback.status == 'Rejected':
                rejected_feedback.append(feedback)
    
    context = {
        'title':'Rejected Paper',
        'rejected_articles':zip(rejected_articles,rejected_feedback),
    }
    return render(request,'users/rejected_articles.html',context)

from django.conf import settings
import os

def article_view(request, pk):
    article = get_object_or_404(Article, pk=pk)
    
    if article.file:
        # Get the absolute file path
        file_path = os.path.join(settings.MEDIA_ROOT, str(article.file))
        
        # Check if file exists
        if os.path.exists(file_path):
            # Get the full URL including domain
            file_url = request.build_absolute_uri(article.file.url)
            print(f"PDF URL: {file_url}")  # Debug print
        else:
            file_url = None
            print(f"File not found at: {file_path}")  # Debug print
    else:
        file_url = None
        print("No file attached to article")  # Debug print
    
    context = {
        'title': article.title,
        'article': article,
        'file_url': file_url
    }
    return render(request, 'users/article-view.html', context)