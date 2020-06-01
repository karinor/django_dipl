from django.shortcuts import render
from django.views.generic import TemplateView, View
from .models import Profile, User
from shop.models import Order, OrderedProducts
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import views
from account.modules.post_actions import PrintableOrders
from .modules.session_save_decorator import SessionSaveDecorator
from django.urls import path
from django.utils.decorators import method_decorator
from dto import settings
# Create your views here.


class ProfileDataView(View):
    template_name = 'profile-data.html'
    def get_context_data(self, **kwargs):
        context = {}
        user = User.objects.get(id=self.request.user.id)
        profile = Profile.objects.get(user=user)
        context['user_data'] = {
                'fullname': user.last_name,
                'email': user.username,
                'phone': profile.phone,
            }
        return context

    def post(self, request, *args, **kwargs):
        username = request.POST.get('email')
        fullname = request.POST.get('fullname')
        phone = request.POST.get('phone')
        user = User.objects.get(id=request.user.id)
        if username is not None and username != request.user.username:
            user.username = username
        if fullname is not None and fullname != request.user.last_name:
            user.last_name = fullname
        if phone is not None:
            profile = Profile.objects.get(user=user)
            profile.phone = phone
            profile.save()
        user.save()
        context = self.get_context_data()
        return render(request, self.template_name, context=context)

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = self.get_context_data()
            return render(request, self.template_name, context=context)
        else:
            return redirect(reverse('account:login'))


class ProfileOrdersView(View):
    template_name = 'profile-orders.html'

    def get_context_data(self, **kwargs):
        context = {}
        orders = Order.objects.filter(user=self.request.user)
        orders_list = PrintableOrders(orders)
        context['orders_list'] = orders_list
        return context

    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            context = self.get_context_data()
            return render(request, self.template_name, context=context)
        else:
            return redirect(reverse('account:login'))


class UserCreationFormModified(UserCreationForm):
    error_css_class = 'simple-form__feedback invalid-feedback'


class RegisterFormView(FormView):
    form_class = UserCreationFormModified
    success_url = '../login'
    template_name = "register.html"


    def form_valid(self, form):
        form.save()
        user = User.objects.get(username=form.cleaned_data['username'])
        profile = Profile(user=user)
        profile.save()
        return super(RegisterFormView, self).form_valid(form)
    

@method_decorator(SessionSaveDecorator((settings.COMPARE_SESSION_ID, settings.FAVORITES_SESSION_ID, settings.CART_SESSION_ID)),name='dispatch')
class LoginView(views.LoginView):
    pass