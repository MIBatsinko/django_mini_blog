from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import redirect
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView, UpdateView
from drf_yasg.utils import swagger_auto_schema
from rest_framework import filters, status
from rest_framework.generics import ListAPIView, RetrieveUpdateAPIView, get_object_or_404, RetrieveAPIView

from .forms import UserProfileForm, UserForm
from .models import UserProfile
from .serializers import UserSerializer, UserResponseSerializer, SingleUserSerializer


class UserApiView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = ['first_name', 'last_name']

    @swagger_auto_schema(responses={status.HTTP_200_OK: UserResponseSerializer()})
    def get(self, request, *args, **kwargs):
        return self.list(request, *args, **kwargs)


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class SingleUserApiView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = SingleUserSerializer


@method_decorator(csrf_exempt, name='dispatch')
class SingleUserUpdateApiView(RetrieveUpdateAPIView):
    queryset = User.objects.all()
    serializer_class = SingleUserSerializer

    def get_object(self):
        return self.request.user


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class UserProfilePageView(TemplateView):
    model = UserProfile
    template_name = 'blog/profile.html'
    context_object_name = 'userprofile'


@method_decorator(login_required(login_url='my_account_login'), name='dispatch')
class UserProfileUpdateView(UpdateView):
    template_name = 'blog/profile_settings.html'

    def get(self, request, *args, **kwargs):
        user = self.request.user
        user_profile_form = UserProfileForm(initial={
                'avatar': user.userprofile.avatar,
            })
        user_profile_form.prefix = 'user_profile_form'
        user_form = UserForm(initial={
                'first_name': user.first_name,
                'email': user.email
            })
        user_form.prefix = 'user_form'
        context = {'user_profile_form': user_profile_form, 'user_form': user_form}
        return self.render_to_response(context)

    def post(self, request, *args, **kwargs):
        user = get_object_or_404(User, username=self.request.user.username)
        user_profile_form = UserProfileForm(self.request.POST, self.request.FILES,
                                            instance=user.userprofile, prefix='user_profile_form')
        user_form = UserForm(self.request.POST, prefix='user_form', instance=user)
        if user_profile_form.is_valid() and user_form.is_valid():
            instance = user_form.save(commit=False)
            instance.save()
            user_profile_form.save()
            return redirect('profile')


class RatingUserPageView(TemplateView):
    model = User
    template_name = 'blog/user_rating.html'
    context_object_name = 'users'

    def get_context_data(self, **kwargs):
        context = super(RatingUserPageView, self).get_context_data(**kwargs)
        context['users'] = User.objects.all()
        return context
