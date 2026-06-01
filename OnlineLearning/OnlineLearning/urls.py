"""
URL configuration for OnlineLearning project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from django.urls import include, path
from django.views.generic import TemplateView

from accounts import views as account_views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include('api.urls')),
    path('api-auth/', include('rest_framework.urls')),
    path('', TemplateView.as_view(template_name='pages/home.html'), name='home'),
    path('about/', TemplateView.as_view(template_name='pages/about.html'), name='about'),
    path('contact/', TemplateView.as_view(template_name='pages/contact.html'), name='contact'),
    path('faq/', TemplateView.as_view(template_name='pages/faq.html'), name='faq'),
    path('testimonials/', TemplateView.as_view(template_name='pages/testimonials.html'), name='testimonials'),
    path('pricing/', TemplateView.as_view(template_name='pages/pricing.html'), name='pricing'),
    path('search/', TemplateView.as_view(template_name='pages/search_results.html'), name='search'),
    path('instructor/', TemplateView.as_view(template_name='pages/instructor.html'), name='instructor'),
    path('profile/', account_views.profile_view, name='profile'),
    path('accounts/', include('accounts.urls')),
    path('accounts/forgot-password/', TemplateView.as_view(template_name='accounts/forgot_password.html'), name='forgot_password'),
    path('accounts/reset-password/', TemplateView.as_view(template_name='accounts/reset_password.html'), name='reset_password'),
    path('accounts/otp/', TemplateView.as_view(template_name='accounts/otp_verification.html'), name='otp_verification'),
    path('accounts/change-password/', account_views.change_password_view, name='change_password'),
    path('accounts/edit-profile/', account_views.edit_profile_view, name='edit_profile'),
    path('courses/', TemplateView.as_view(template_name='courses/course_list.html'), name='courses'),
    path('courses/<slug:slug>/', TemplateView.as_view(template_name='courses/course_detail.html'), name='course_detail'),
    path('categories/', TemplateView.as_view(template_name='categories/categories.html'), name='categories'),
    path('dashboard/student/', login_required(TemplateView.as_view(template_name='dashboard/student_dashboard.html')), name='student_dashboard'),
    path('dashboard/instructor/', login_required(TemplateView.as_view(template_name='dashboard/instructor_dashboard.html')), name='instructor_dashboard'),
]

handler404 = 'OnlineLearning.views.error_404'
handler500 = 'OnlineLearning.views.error_500'
