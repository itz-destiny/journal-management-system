
import datetime
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from .forms import LoginForm
from apps.user.models import STATUS_ADMIN_PUBLISHED, NormalUser,Article
from apps.admin_user.models import Category,Notice
from apps.reviewer.models import STATUS_ACCEPTED, STATUS_REJECTED, STATUS_REVIEWER_PUBLISHED, STATUS_UNDER_REVIEW, Reviewer
from datetime import datetime, timedelta, time
from apps.user.filters import ArticleFilter
from django.core.paginator import Paginator
from django.core.paginator import EmptyPage
from django.core.paginator import PageNotAnInteger


def landing_page(request):
    # Modern landing page for non-authenticated users
    if not request.user.is_authenticated:
        return render(request, 'landing_page.html')
    else:
        return redirect('home')

def first_page(request):
    # Show modern landing page for non-authenticated users
    if not request.user.is_authenticated:
        return render(request, 'landing_page.html')
    
    # Show published articles for authenticated users
    categories = Category.objects.all()
    published_articles = Article.objects.filter(status = STATUS_ADMIN_PUBLISHED).order_by('-updated_at')
    
    filter_form = ArticleFilter()
    title = request.GET.get('title')
    category = request.GET.get('category')
    
    if title or category:
        filter_articles = ArticleFilter(request.GET, queryset=published_articles).qs
        context = {
            'title':'Journal Management System',
            'category':Category.objects.all(),
            'published_articles':filter_articles,
            'filter_form':filter_form,
        }
        return render(request,'home.html',context)
        
    page = request.GET.get('page', 1)
    paginator = Paginator(published_articles, 10)  # Changed from 1 to 10 per page
    try:    
        published_articles = paginator.page(page)
    except PageNotAnInteger:
        published_articles = paginator.page(1)
    except EmptyPage:
        published_articles = paginator.page(paginator.num_pages)
    
    context = {
        'title':'Journal Management System',
        'category':categories,
        'published_articles':published_articles,
        'filter_form':filter_form,
        'notice': Notice.objects.filter(status=True).first(),
    }
    
    return render(request,'home.html',context)


def dashboard(request):
    today = datetime.now().date()
    tomorrow = today + timedelta(1)
    today_start = datetime.combine(today, time())
    today_end = datetime.combine(tomorrow, time())
    
    # Determine user role and route to appropriate dashboard
    user_groups = request.user.groups.all()
    
    # Check if user is admin or superuser
    if request.user.is_superuser or (user_groups and user_groups[0].name == 'Admin'):
        # Admin Dashboard
        from apps.permissions.models import CustomUser
        
        users = NormalUser.objects.all()
        reviewers = Reviewer.objects.all()
        all_users = CustomUser.objects.all().order_by('-date_joined')
        all_articles = Article.objects.all().order_by('-created_at')
        unpublish_articles_by_admin = Article.objects.filter(status=STATUS_REVIEWER_PUBLISHED)
        today_publish_by_admin = Article.objects.filter(status=STATUS_ADMIN_PUBLISHED, updated_at__gte=today_start).filter(updated_at__lte=today_end)
        recent_articles = Article.objects.all().order_by('-created_at')[:5]
        
        context = {
            'title': 'Admin Dashboard',
            'normaluser_count': users.count(),
            'reviewer_count': reviewers.count(),
            'unpublish_count': unpublish_articles_by_admin.count(),
            'today_publish_count': today_publish_by_admin.count(),
            'all_users': all_users,
            'articles': all_articles,
            'total_count': all_articles.count(),
            'recent_articles': recent_articles,
        }
        return render(request, 'admin_dashboard.html', context)
    
    # Check if user is editor
    elif user_groups and user_groups[0].name == 'Editor':
        # Editor Dashboard
        all_articles = Article.objects.all()
        
        context = {
            'title': 'Editor Dashboard',
            'total_submitted': all_articles.count(),
            'under_review': all_articles.filter(status=STATUS_UNDER_REVIEW).count(),
            'decision_ready': all_articles.filter(status=STATUS_REVIEWER_PUBLISHED).count(),
            'accepted': all_articles.filter(status=STATUS_ADMIN_PUBLISHED).count(),
        }
        return render(request, 'editor_dashboard.html', context)
    
    # Check if user is reviewer
    elif user_groups and user_groups[0].name == 'Reviewer':
        # Reviewer Dashboard
        today_accepted_article_by_reviewer = Article.objects.filter(status=STATUS_ACCEPTED, updated_at__gte=today_start).filter(updated_at__lte=today_end)
        today_rejected_article_by_reviewer = Article.objects.filter(status=STATUS_REJECTED, updated_at__gte=today_start).filter(updated_at__lte=today_end)
        today_publish_article_to_admin = Article.objects.filter(status=STATUS_REVIEWER_PUBLISHED, updated_at__gte=today_start).filter(updated_at__lte=today_end)
        article_under_review = Article.objects.filter(status=STATUS_UNDER_REVIEW)

        accepted_count = today_accepted_article_by_reviewer.count()
        rejected_count = today_rejected_article_by_reviewer.count()
        published_count = today_publish_article_to_admin.count()
        pending_count = article_under_review.count()

        recent_articles = article_under_review.order_by('-created_at')[:5]

        notifications = []
        if pending_count:
            notifications.append({
                'level': 'warning',
                'icon': 'fa-hourglass-half',
                'title': 'Pending Reviews',
                'message': f'You have {pending_count} manuscript{"s" if pending_count != 1 else ""} waiting for review.'
            })
        else:
            notifications.append({
                'level': 'info',
                'icon': 'fa-check-circle',
                'title': 'All Clear',
                'message': 'No manuscripts are waiting for review right now.'
            })

        if accepted_count:
            notifications.append({
                'level': 'success',
                'icon': 'fa-check',
                'title': 'Accepted Today',
                'message': f'{accepted_count} manuscript{"s" if accepted_count != 1 else ""} accepted today.'
            })

        if rejected_count:
            notifications.append({
                'level': 'danger',
                'icon': 'fa-times',
                'title': 'Rejected Today',
                'message': f'{rejected_count} manuscript{"s" if rejected_count != 1 else ""} rejected today.'
            })

        if published_count:
            notifications.append({
                'level': 'info',
                'icon': 'fa-paper-plane',
                'title': 'Forwarded to Admin',
                'message': f'{published_count} manuscript{"s" if published_count != 1 else ""} sent to the admin today.'
            })
        
        context = {
            'title': 'Reviewer Dashboard',
            'today_accepted_article_by_reviewer_count': accepted_count,
            'today_rejected_article_by_reviewer_count': rejected_count,
            'today_publish_article_to_admin_count': published_count,
            'article_under_review_count': pending_count,
            'recent_articles': recent_articles,
            'notifications': notifications,
        }
        return render(request, 'reviewer_dashboard.html', context)
    
    # Default to author/user dashboard
    else:
        # Author Dashboard
        total_user_articles_submitted = Article.objects.filter(user=request.user)
        total_user_article_accepted = Article.objects.filter(user=request.user, status=STATUS_ADMIN_PUBLISHED)
        total_user_article_rejected = Article.objects.filter(user=request.user, status=STATUS_REJECTED)
        total_user_article_under_review = Article.objects.filter(user=request.user, status=STATUS_UNDER_REVIEW)
        
        context = {
            'title': 'Author Dashboard',
            'total_user_articles_submitted_count': total_user_articles_submitted.count(),
            'total_user_article_accepted_count': total_user_article_accepted.count(),
            'total_user_article_rejected_count': total_user_article_rejected.count(),
            'total_user_article_under_review_count': total_user_article_under_review.count(),
        }
        return render(request, 'author_dashboard.html', context)


def user_login(request):

    form = LoginForm()

    if request.method == "POST":
        
        username = request.POST.get("username")
        password = request.POST.get("password1")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            if group or request.user.is_superuser:
                return redirect('home')
            else:
                messages.error(request, "Invalid User")
                return redirect('login')
        else:
            messages.error(request, "Invalid Login Details")
            return redirect('login')

    return render(request, 'login.html', {'form': form})



def user_logout(request):
    logout(request)
    return redirect('login')

def debug_user_info(request):
    return render(request, 'debug_user.html')