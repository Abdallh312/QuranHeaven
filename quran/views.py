from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .decorators import user_not_authenticated,user_is_superuser,user_is_authenticated,user_is_not_subscribe,user_is_subscribe,only_once,cannot_make_order
from django.contrib.auth import get_user_model
from django.contrib.auth.models import User
from typing import Protocol
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate, get_user_model
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.core.mail import EmailMessage
from django.db.models.query_utils import Q
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from .models import *
from .forms import *
from .decorators import user_not_authenticated
from .tokens import account_activation_token
from django.contrib import messages
from django.core.mail import EmailMessage
from django.shortcuts import render, get_object_or_404
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.decorators import login_required
def astmaa(request):
    return render(request,'astmaa.html')

def reads(request):
    return render(request,'reads.html')

@login_required
def donate(request):
    return render(request, 'donate.html')
@login_required
def payment_yearly(request):
    if request.method == 'POST':
        form = WallEntryForm_200(request.POST, request.FILES)
        if form.is_valid():
            wall_entry = form.save(commit=False)
            wall_entry.user = request.user 
            wall_entry.save()
            messages.success(request, "Your order has been placed successfully.")
            return redirect('home')
        
    else:
        form = WallEntryForm_200()
    
    return render(request, 'payment_yearly.html', {'form': form})
@login_required
def payment(request):
    if request.method == 'POST':
        form = WallEntryForm_100(request.POST, request.FILES)
        if form.is_valid():
            wall_entry = form.save(commit=False)
            wall_entry.user = request.user 
            wall_entry.save()
            messages.success(request, "<div class='alert alert-warning'>Your order has been placed successfully.</div>")
            return redirect('home')
        
    else:
        form = WallEntryForm_100()
    
    return render(request, 'payment.html', {'form': form})
@login_required
def plan_list(request):
    return render(request, 'subscribe.html')

@user_is_not_subscribe
def exchange_details(request):
    if request.method == 'POST':
        form = WallEntryForm(request.POST, request.FILES)
        if form.is_valid():
            wall_entry = form.save(commit=False)
            wall_entry.user = request.user 
            wall_entry.save()
            return redirect('home')
        messages.success(request, "Your order has been placed successfully.")
    else:
        form = WallEntryForm()
    
    return render(request, 'donate.html', {'form': form})
@user_is_subscribe
def submit_fatwa(request):
    if not request.session.get('fatwa_count', 0) < 6:
        messages.error(request, "You have already submitted 3 questions.")
        return redirect('home')
    request.session['fatwa_count'] = request.session.get('fatwa_count', 0) + 1
    if request.method == "POST":
        form = FatwaForm(request.POST)
        if form.is_valid():
            question = form.cleaned_data['question']
            category = form.cleaned_data.get('category', '')
            Fatwa.objects.create(question=question, category=category)
            messages.success(request, "<div class='alert alert-warning'>Your question has been submitted.</div>")
            return redirect('home')
    else:
        form = FatwaForm()

    return render(request, 'submit_fatwa.html', {'form': form})
@user_is_superuser
def fatwa_list(request):
    fatwas = Fatwa.objects.all().order_by('-date')
    return render(request, 'fatwa_list.html', {'fatwas': fatwas})

@user_is_superuser
def fatwa_detail(request, fatwa_id):
    fatwa = get_object_or_404(Fatwa, id=fatwa_id)
    return render(request, 'fatwa_detail.html', {'fatwa': fatwa})
@login_required
def contact(request):
    return render(request, 'contact.html')
@login_required
def about(request):
    return render(request, 'about.html')
def activate(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()

        messages.success(request, "<div class='alert alert-warning'>Thank you for your email confirmation. Now you can login your account</div>")
        return redirect('login')
    else:
        messages.error(request, "Activation link is invalid!")

    return redirect('home')
def success(request):
    messages.success(request, "Your order done our team withh contact you")
    return render(request, 'success.html')
@user_is_subscribe
@cannot_make_order
def make_order(request):
    if request.method == 'POST':
        form = orderformm(request.POST, request.FILES)
        if form.is_valid():
            wall_entry = form.save(commit=False)
            wall_entry.user = request.user 
            wall_entry.save()
            messages.success(request, "<div class='alert alert-warning'>Your order has been placed successfully.</div>")
            return redirect('home')
        
    else:
        form = orderformm()
    
    return render(request, 'make_order.html', {'form': form})

def activateEmail(request, user, to_email):
    mail_subject = "Activate your user account."
    message = render_to_string("template_activate_account.html", {
        'user': user.username,
        'domain': get_current_site(request).domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
        "protocol": 'https' if request.is_secure() else 'http'
    })
    email = EmailMessage(mail_subject, message, to=[to_email])
    if email.send():
        messages.success(request, f"<div class='alert alert-warning'> Dear <b>{user}</b>, please go to you email <b>{to_email}</b> inbox and click on \
                received activation link to confirm and complete the registration. <b>Note:</b> Check your spam folder </div>")
    else:
        messages.error(request, f'Problem sending email to {to_email}, check if you typed it correctly.')

@login_required

def home_view(request):
    matching_series = ArticleSeries.objects.all()
    return render(
        request=request,
        template_name='home.html',
        context={"objects": matching_series
                ,'type': 'series'},
        
        )
@user_is_subscribe
def series(request, series: str):
    matching_series = Article.objects.filter(series__slug=series).all()
    
    return render(
        request=request,
        template_name='home.html',
        context={"objects": matching_series,'type': 'article'},
        )
@user_is_subscribe
def article(request, series: str, article: str):
    matching_article = Article.objects.filter(series__slug=series, article_slug=article).first()
    
    return render(
        request=request,
        template_name='article.html',
        context={"object": matching_article}
        )

@user_not_authenticated
def signup_view(request):
    if request.method == "POST":
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active=False
            user.save()
            activateEmail(request, user, form.cleaned_data.get('email'))
            return redirect('home')

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    else:
        form = UserRegistrationForm()

    return render(
        request=request,
        template_name="signup.html",
        context={"form": form}
        )

def welcome_view(request):
        if request.user.is_authenticated:
            return redirect('home') 
        return render(request, 'welcomepage.html')
@user_not_authenticated
def custom_login(request):
    if request.method == "POST":
        form = UserLoginForm(request=request, data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data["username"],
                password=form.cleaned_data["password"],
            )
            if user is not None:
                login(request, user)
                messages.success(request, f" Hello {user.username}! You have been logged in")
                return redirect("home")

        else:
            for key, error in list(form.errors.items()):
                if key == 'captcha' and error[0] == 'This field is required.':
                    messages.error(request, "You must pass the reCAPTCHA test")
                    continue
                
                messages.error(request, error) 

    form = UserLoginForm()

    return render(
        request=request,
        template_name="login.html",
        context={"form": form}
        )

@login_required

def profile(request, username):
    if request.method == 'POST':
        user = request.user
        form = UserUpdateForm(request.POST, request.FILES, instance=user)
        if form.is_valid():
            user_form = form.save()

            messages.success(request, f"<div class='alert alert-warning'>{user_form}, Your profile has been updated!</div>")
            return redirect('profile', user_form.username)

        for error in list(form.errors.values()):
            messages.error(request, error)

    user = get_user_model().objects.filter(username=username).first()
    if user:
        form = UserUpdateForm(instance=user)
        form.fields['description'].widget.attrs = {'rows': 1}
        return render(request, 'profile.html', context={'form': form})

    return redirect("home")
def logout_view(request):
    logout(request)
    return redirect('welcome')

@user_is_superuser
def new_series(request):
    if request.method == "POST":
        form = SeriesCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = SeriesCreateForm()

    return render(
        request=request,
        template_name='new_record.html',
        context={
            "object": "sheik",
            "form": form
            }
        )
def subscribe(request):
    if request.method == 'POST':
        name = request.POST.get('name', None)
        email = request.POST.get('email', None)

        if not name or not email:
            messages.error(request, "You must type legit name and email to subscribe to a Newsheik")
            return redirect("/")

        if get_user_model().objects.filter(email=email).first():
            messages.error(request, f"Found registered user with associated {email} email. You must login to subscribe or unsubscribe.")
            return redirect(request.META.get("HTTP_REFERER", "/")) 

        subscribe_user = SubscribedUsers.objects.filter(email=email).first()
        if subscribe_user:
            messages.error(request, f"{email} email address is already subscriber.")
            return redirect(request.META.get("HTTP_REFERER", "/"))  

        try:
            validate_email(email)
        except ValidationError as e:
            messages.error(request, e.messages[0])
            return redirect("/")

        subscribe_model_instance = SubscribedUsers()
        subscribe_model_instance.name = name
        subscribe_model_instance.email = email
        subscribe_model_instance.save()
        messages.success(request, f'{email} email was successfully subscribed to our newsletter!')
        return redirect(request.META.get("HTTP_REFERER", "/"))

@user_is_superuser
def newsletter(request):
    if request.method == 'POST':
        form = NewsletterForm(request.POST)
        if form.is_valid():
            subject = form.cleaned_data.get('subject')
            receivers = form.cleaned_data.get('receivers').split(',')
            email_message = form.cleaned_data.get('message')

            mail = EmailMessage(subject, email_message, f"PyLessons <{request.user.email}>", bcc=receivers)
            mail.content_subtype = 'html'

            if mail.send():
                messages.success(request, "Email sent succesfully")
            else:
                messages.error(request, "There was an error sending email")

        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

        return redirect('/')

    form = NewsletterForm()
    form.fields['receivers'].initial = ','.join([active.email for active in SubscribedUsers.objects.all()])
    return render(request=request, template_name='main/newsletter.html', context={'form': form})
@user_is_superuser

def series_update(request, series):
    matching_series = ArticleSeries.objects.filter(slug=series).first()

    if request.method == "POST":
        form = SeriesUpdateForm(request.POST, request.FILES, instance=matching_series)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    else:
        form = SeriesUpdateForm(instance=matching_series)

        return render(
            request=request,
            template_name='new_record.html',
            context={
                "object": "sheik",
                "form": form
                }
            )

@user_is_superuser

def series_delete(request, series):
    matching_series = ArticleSeries.objects.filter(slug=series).first()

    if request.method == "POST":
        matching_series.delete()
        return redirect('/')
    else:
        return render(
            request=request,
            template_name='confirm_delete.html',
            context={
                "object": matching_series,
                "type": "sheik"
                }
            )

@user_is_superuser

def article_update(request, series, article):
    matching_article = Article.objects.filter(series__slug=series, article_slug=article).first()

    if request.method == "POST":
        form = ArticleUpdateForm(request.POST, request.FILES, instance=matching_article)
        if form.is_valid():
            form.save()
            return redirect(f'/{matching_article.slug}')
    
    else:
        form = ArticleUpdateForm(instance=matching_article)

        return render(
            request=request,
            template_name='new_record.html',
            context={
                "object": "gategory",
                "form": form
                }
            )

@user_is_superuser
def article_delete(request, series, article):
    matching_article = Article.objects.filter(series__slug=series, article_slug=article).first()

    if request.method == "POST":
        matching_article.delete()
        return redirect('/')
    else:
        return render(
            request=request,
            template_name='confirm_delete.html',
            context={
                "object": matching_article,
                "type": "gategory"
                }
            )
@user_is_superuser

def new_series(request):
    if request.method == "POST":
        form = SeriesCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect("home")

    else:
        form = SeriesCreateForm()

    return render(
        request=request,
        template_name='new_record.html',
        context={
            "object": "sheik",
            "form": form
            }
        )

@user_is_superuser

def new_post(request):
    if request.method == "POST":
        form = ArticleCreateForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    else:
        form = ArticleCreateForm()

    return render(
        request=request,
        template_name='new_record.html',
        context={
            "object": "Gatergory",
            "form": form
            }
        )

@user_is_superuser

def series_update(request, series):
    matching_series = ArticleSeries.objects.filter(slug=series).first()

    if request.method == "POST":
        form = SeriesUpdateForm(request.POST, request.FILES, instance=matching_series)
        if form.is_valid():
            form.save()
            return redirect('home')
    
    else:
        form = SeriesUpdateForm(instance=matching_series)

        return render(
            request=request,
            template_name='new_record.html',
            context={
                "object": "Series",
                "form": form
                }
            )

@user_is_superuser
def series_delete(request, series):
    matching_series = ArticleSeries.objects.filter(slug=series).first()

    if request.method == "POST":
        matching_series.delete()
        return redirect('/')
    else:
        return render(
            request=request,
            template_name='confirm_delete.html',
            context={
                "object": matching_series,
                "type": "Series"
                }
            )

@user_is_superuser
def article_update(request, series, article):
    matching_article = Article.objects.filter(series__slug=series, article_slug=article).first()

    if request.method == "POST":
        form = ArticleUpdateForm(request.POST, request.FILES, instance=matching_article)
        if form.is_valid():
            form.save()
            return redirect(f'/{matching_article.slug}')
    
    else:
        form = ArticleUpdateForm(instance=matching_article)

        return render(
            request=request,
            template_name='new_record.html',
            context={
                "object": "Article",
                "form": form
                }
            )

@user_is_superuser
def article_delete(request, series, article):
    matching_article = Article.objects.filter(series__slug=series, article_slug=article).first()

    if request.method == "POST":
        matching_article.delete()
        return redirect('/')
    else:
        return render(
            request=request,
            template_name='confirm_delete.html',
            context={
                "object": matching_article,
                "type": "article"
                }
            )
@login_required
def password_change(request):
    user = request.user
    if request.method == 'POST':
        form = SetPasswordForm(user, request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, "Your password has been changed")
            return redirect('login')
        else:
            for error in list(form.errors.values()):
                messages.error(request, error)

    form = SetPasswordForm(user)
    return render(request, 'password_reset_confirm.html', {'form': form})

@user_not_authenticated
def password_reset_request(request):
    if request.method == 'POST':
        form = PasswordResetForm(request.POST)
        if form.is_valid():
            user_email = form.cleaned_data['email']
            associated_user = get_user_model().objects.filter(Q(email=user_email)).first()
            if associated_user:
                subject = "Password Reset request"
                message = render_to_string("template_reset_password.html", {
                    'user': associated_user,
                    'domain': get_current_site(request).domain,
                    'uid': urlsafe_base64_encode(force_bytes(associated_user.pk)),
                    'token': account_activation_token.make_token(associated_user),
                    "protocol": 'https' if request.is_secure() else 'http'
                })
                email = EmailMessage(subject, message, to=[associated_user.email])
                if email.send():
                    messages.success(request,
                        """
                        Password reset sent
                        
                            We've emailed you instructions for setting your password, if an account exists with the email you entered. 
                            You should receive them shortly.If you don't receive an email, please make sure you've entered the address 
                            you registered with, and check your spam folder.
                        
                        """
                    )
                else:
                    messages.error(request, "Problem sending reset password email, <b>SERVER PROBLEM</b>")

            return redirect('home')

        for key, error in list(form.errors.items()):
            if key == 'captcha' and error[0] == 'This field is required.':
                messages.error(request, "You must pass the Recapthca test")
                continue

    form = PasswordResetForm()
    return render(
        request=request, 
        template_name="password_reset.html", 
        context={"form": form}
        )

def passwordResetConfirm(request, uidb64, token):
    User = get_user_model()
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except:
        user = None

    if user is not None and account_activation_token.check_token(user, token):
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, "Your password has been set. You may go ahead and <b>log in </b> now.")
                return redirect('home')
            else:
                for error in list(form.errors.values()):
                    messages.error(request, error)

        form = SetPasswordForm(user)
        return render(request, 'password_reset_confirm.html', {'form': form})
    else:
        messages.error(request, "Link is expired")

    messages.error(request, 'Something went wrong, redirecting back to Homepage')
    return redirect("home")