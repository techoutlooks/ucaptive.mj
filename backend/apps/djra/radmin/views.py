from django.template import RequestContext
from django.shortcuts import render_to_response, get_object_or_404
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect, HttpResponseForbidden,HttpResponse,HttpResponseBadRequest
from django.http import HttpResponseNotFound

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from django.views.generic.edit import UpdateView
from lib.mixins.views.angular import NgFormViewMixin

from djra.freeradius.models import Radusergroup,Radcheck,Radgroupcheck,Radacct
from djra.freeradius.models import RadUser, get_groups, get_radgroup_count, get_group, RadGroup
from djra.radmin.forms import RadUserFilterForm,RadUserForm,NewRadUserForm
from djra.radmin.forms import NewRadGroupForm,RadGroupForm


# @login_required
def home(request):
    user_count = RadUser.objects.count_info()
    group_count = get_radgroup_count()
    return render_to_response(
        'radmin/home.html',
        {'active_user_count' : user_count['active'],
         'suspended_user_count' : user_count['suspended'],
         'group_count' : group_count,
        },
        context_instance = RequestContext(request)
    )


# @login_required
def users(request):
    query_set = RadUser.objects.all()
    filter_form = RadUserFilterForm(request.GET)
    if filter_form.is_valid():
        is_active = filter_form.cleaned_data.get('is_active', '')
        if is_active == '1':
            query_set = query_set.filter_is_active(True)
        elif is_active == '0':
            query_set = query_set.filter_is_active(False)
            
        is_online = filter_form.cleaned_data.get('is_online', '')
        if is_online == '0':
            query_set = query_set.filter_is_online(False)
        elif is_online == '1':
            query_set = query_set.filter_is_online(True)
 
        q = filter_form.cleaned_data.get('username', '')
        if q:
            query_set = query_set.filter(username__icontains=q)
    return render_to_response(
        'radmin/users.html',
        {'query_set' : query_set, 'filter_form' : filter_form, 'request' : request},
        context_instance = RequestContext(request)
    )


class UserDetailView(NgFormViewMixin, UpdateView):
    model = RadUser

    template_name = 'radmin/user_detail.html'
    form_class = RadUserForm
    pk_url_kwarg = 'username'

    def get_object(self):
        return get_object_or_404(RadUser, username=self.kwargs.get(self.pk_url_kwarg))

    def form_valid(self, form):
        raduser = self.object
        assert raduser.username == form.cleaned_data['username']
        raduser.update(password=form.cleaned_data['password'],
                       is_active=form.cleaned_data['is_active'],
                       groups=form.cleaned_data['groups'].split(','))
        messages.success(self.request, 'User %s saved.' % raduser.username)
        return HttpResponseRedirect(reverse('djra.radmin.views.user_detail', kwargs={'username': username}))


# @login_required
def user_sessions(request, username):

    try:
        raduser = RadUser.objects.get(username=username)
    except RadUser.DoesNotExist:
        return HttpResponseNotFound('not found')
    sessions =  Radacct.objects.filter(username=username).order_by('-acctstarttime')
    return render_to_response(
        'radmin/user_sessions.html',
        {'raduser' : raduser, 'sessions' : sessions, 'request' : request},
        context_instance = RequestContext(request)
    )


# @login_required
def create_user(request):
    if request.method == 'POST':
        form = NewRadUserForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data['username']
            raduser, created = RadUser.objects.get_or_create(username=username,
                                                             defaults={'value' : form.cleaned_data['password']})
            if not created:
                messages.error(request, 'User %s already exists.' %username)
            else:    
                raduser.update(password=form.cleaned_data['password'],
                            is_active=form.cleaned_data['is_active'],
                            groups=form.cleaned_data['groups'].split(','))
                messages.success(request, 'User %s created.' %username)
                return HttpResponseRedirect(reverse('djra.radmin.views.user_detail', kwargs={'username' : username}))
    else:
        form = NewRadUserForm()
        
    return render_to_response(
        'radmin/create_user.html',
        {'form' : form, 'request' : request},
        context_instance = RequestContext(request)
    )


# @login_required
def groups(request):
    groups = get_groups()
    return render_to_response(
        'radmin/groups.html',
        {'groups' : groups, 'request' : request},
        context_instance = RequestContext(request)
    )


# @login_required
def create_group(request):
    if request.method == 'POST':
        form = NewRadGroupForm(request.POST)
        if form.is_valid():
            groupname=form.cleaned_data['groupname']
            simultaneous_use=form.cleaned_data['simultaneous_use']
            gd = RadGroup(groupname=groupname)
            gd.set_simultaneous_use(simultaneous_use)

            messages.success(request, 'Group %s created.' %groupname)
            return HttpResponseRedirect(reverse('djra.radmin.views.group_detail', kwargs={'groupname' : groupname}))
    else:
        form = NewRadGroupForm()
        
    return render_to_response(
        'radmin/create_group.html',
        {'form' : form, 'request' : request},
        context_instance = RequestContext(request)
    )


# @login_required
def group_detail(request, groupname):
    radgroup = get_group(groupname)
    if radgroup is None:
        return HttpResponseNotFound('not found')

    if request.method == 'POST':
        form = RadGroupForm(request.POST)
        if form.is_valid():
            assert groupname == form.cleaned_data['groupname']
            simultaneous_use=form.cleaned_data['simultaneous_use']
            gd = RadGroup(groupname=groupname)
            gd.set_simultaneous_use(simultaneous_use)

            messages.success(request, 'Group %s updated.' %groupname)
            return HttpResponseRedirect(reverse('djra.radmin.views.group_detail', kwargs={'groupname' : groupname}))
    else:
        form = RadGroupForm({
            'groupname' : groupname,
            'simultaneous_use' : RadGroup(groupname).simultaneous_use
        })
 
    return render_to_response(
        'radmin/group_detail.html',
        {'group' : radgroup, 'form' : form, 'request' : request},
        context_instance = RequestContext(request)
    )

