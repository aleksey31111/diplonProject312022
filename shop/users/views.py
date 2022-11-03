from django.shortcuts import render, redirect
from django.contrib import auth, messages
from django.contrib.auth.decorators import login_required

from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template

from django.conf import settings
from django.core.mail import send_mail

from products.models import Basket
from users.forms import UserLoginForm, UserRegistrationForm, UserProfileForm
from .forms import ContactForm


def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = auth.authenticate(username=username, password=password)
            if user and user.is_active:
                auth.login(request, user)
                return redirect('index')
    else:
        form = UserLoginForm()
    context = {
        'form': form
    }
    return render(request, 'users/login.html', context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            messages.success(request,
                             'Вы успешно зарегистрировались на сайте '
                             'Магазин Устройств')
            return redirect('login')
    else:
        form = UserRegistrationForm
    context = {'form': form}
    return render(request, 'users/register.html', context)


@login_required(login_url='/users/login')
def profile(request):
    user = request.user
    if request.method == "POST":
        form = UserProfileForm(
            data=request.POST,
            files=request.FILES,
            instance=user)
        if form.is_valid():
            form.save()
            return redirect('profile')
    else:
        form = UserProfileForm(instance=user)

    baskets = Basket.objects.filter(user=user)
    total_quantity = sum(basket.quantity for basket in baskets)
    total_sum = sum(basket.sum() for basket in baskets)
    context = {
        'form': form,
        'baskets': Basket.objects.filter(user=user),
        'total_quantity': total_quantity,
        'total_sum': total_sum,
    }
    return render(request, 'users/profile.html', context)


def logout(request):
    auth.logout(request)
    return redirect('index')


@login_required(login_url='/users/login')
def contacts(request):
    context = {}
    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            send_message(
                form.cleaned_data['name'],
                form.cleaned_data['email'],
                form['message'],
            )
    else:
        form = ContactForm()
    context['form'] = form
    return render(
        request,
        'users/contacts.html',
        context=context
    )


def send_message(name, email, message):
    text = get_template('users/message.html')
    html = get_template('users/message.html')
    context = {'name': name,
               'email': email,
               'message': message}
    subject = 'Сообщение от пользователя'
    from_email = 'bashkirov1985@internet.ru'
    text_content = text.render(context)
    html_content = html.render(context)

    msg = EmailMultiAlternatives(subject, text_content, from_email, ['bashkirov1985@internet.ru'])
    msg.attach_alternative(html_content, 'text/html')
    msg.send()
    # send_mail('Тема', 'Тело письма', settings.EMAIL_HOST_USER, ['to@example.com'])
