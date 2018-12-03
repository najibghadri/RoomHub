from django.contrib.auth.decorators import login_required, user_passes_test
from django.utils.decorators import method_decorator

from django.urls import reverse_lazy
from django.views import generic

from .models import Room, CustomUser, Event
from .forms import CustomUserCreationForm, CustomUserChangeForm

from django.contrib.auth.mixins import UserPassesTestMixin

from django.http import HttpResponse, HttpResponseNotFound

from django.db.models import Q


def test_view_permission(self):
    return self.get_object().is_public or self.get_object().organizer_user == self.request.user
                       

def test_edit_permission(self):
    return self.get_object().organizer_user == self.request.user


class EventList(generic.ListView):
    model = Event
    template_name = 'rooms/index.html'
    context_object_name = 'events'

    def get_queryset(self):
        if self.request.user.is_authenticated:
            return Event.objects.filter(Q(is_public=True) | Q(organizer_user=self.request.user)).order_by('start')
        else:
            return Event.objects.filter(Q(is_public=True)).order_by('start')
            

class SignUp(generic.CreateView):
    form_class = CustomUserCreationForm
    success_url = reverse_lazy('rooms:login')
    template_name = 'registration/signup.html'


@method_decorator(login_required, name='dispatch')
class Profile(generic.DetailView):
    model = CustomUser
    template_name = 'rooms/profile.html'

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.request.user.id)


@method_decorator(login_required, name='dispatch')
class EditProfile(generic.UpdateView):
    form_class = CustomUserChangeForm
    success_url = reverse_lazy('rooms:profile')
    template_name = 'rooms/edit_profile.html'

    def get_object(self, queryset=None):
        return CustomUser.objects.get(id=self.request.user.id)


@method_decorator(login_required, name='dispatch')
class MyEventList(generic.ListView):
    model = Event
    template_name = 'rooms/my-events.html'
    context_object_name = 'events'

    def get_queryset(self):
        return Event.objects.filter(organizer_user=self.request.user)
       


@method_decorator(login_required, name='dispatch')
class EventDetail(UserPassesTestMixin, generic.DetailView):
    model = Event
    template_name = 'rooms/event_detail.html'
    
    def handle_no_permission(self):
        return HttpResponseNotFound()
    
    def test_func(self):
        return test_view_permission(self) 
        


@method_decorator(login_required, name='dispatch')
class EventCreate(generic.CreateView):
    model = Event
    fields = ('title','description','start', 'end','room','is_public') 
    template_name = 'rooms/event_new.html'  

    def get_success_url(self):
        return reverse_lazy('rooms:event_detail', args=(self.object.id,))
    
    def form_valid(self, form):
        instance = form.save(commit=False)
        instance.organizer_user = self.request.user
        return super().form_valid(form)



@method_decorator(login_required, name='dispatch')
class EventEdit(UserPassesTestMixin, generic.UpdateView):
    model = Event
    fields = ('title','description','start', 'end','room','is_public') 
    template_name = 'rooms/event_edit.html'

    def test_func(self):
        return test_edit_permission(self)  
    
    def get_success_url(self):
        return reverse_lazy('rooms:event_detail', args=(self.object.id,))


@method_decorator(login_required, name='dispatch')
class EventDelete(UserPassesTestMixin, generic.DeleteView):
    model = Event
    success_url = reverse_lazy('rooms:home')
    template_name = 'rooms/event_delete.html'

    def test_func(self):
        return test_edit_permission(self)  


from django.contrib import messages
from django.contrib.auth import update_session_auth_hash
from django.contrib.auth.forms import PasswordChangeForm
from django.shortcuts import render, redirect

def change_password(request):
    if request.method == 'POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            update_session_auth_hash(request, user)  # Important!
            messages.success(request, 'Your password was successfully updated!')
            return redirect('rooms:profile')
        else:
            messages.error(request, 'Please correct the error below.')
    else:
        form = PasswordChangeForm(request.user)
    return render(request, 'registration/password_change.html', {
        'form': form
    })






@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class RoomList(generic.ListView):
    model = Room
    template_name = 'rooms/rooms.html'
    context_object_name = 'rooms'


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class RoomCreate(generic.CreateView):
    model = Room
    fields = ('name',)
    template_name = 'rooms/room_new.html'  

    def get_success_url(self):
        return reverse_lazy('rooms:rooms')
    

@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class RoomEdit(generic.UpdateView):
    model = Room
    fields = ('name',) 
    template_name = 'rooms/room_edit.html'
    
    def get_success_url(self):
        return reverse_lazy('rooms:rooms')


@method_decorator(user_passes_test(lambda u: u.is_superuser), name='dispatch')
class RoomDelete(generic.DeleteView):
    model = Room
    success_url = reverse_lazy('rooms:rooms')
    template_name = 'rooms/room_delete.html'

    def get_context_data(self, **kwargs):
        data = super().get_context_data(**kwargs)
        data['events_in_room'] = Event.objects.filter(room=data['object'])
        return data
  