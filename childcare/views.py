from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic import CreateView
from guardian.decorators import permission_required_or_403
from guardian.shortcuts import assign_perm
from .forms import ChildcareCreateForm, ChildcareNewsCreateForm, ClassroomCreateForm
from .models import Childcare, ChildcareNews, Classroom


class ChildcareCreate(CreateView):
    form_class = ChildcareCreateForm
    template_name = 'childcare/childcare_create.html'

    def form_valid(self, form):
        obj = form.save(commit=False)
        obj.manager = self.request.user
        obj.save
        self.object = obj
        form.save(commit=True)
        childcare = self.object
        manager = self.request.user
        group = Group.objects.get(name='%s: Manager' % childcare.slug)
        manager.groups.add(group)
        return HttpResponseRedirect(self.get_success_url())


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'pk', 'pk'))
def childcare(request, pk):
    childcare = get_object_or_404(Childcare, pk=pk)
    childcare_news = ChildcareNews.objects.filter(childcare=childcare)
    classroom_list = Classroom.objects.filter(childcare=childcare)
    return render(request, 'childcare/childcare_detail.html', {'childcare': childcare,
                                                               'news_list': childcare_news,
                                                               'classroom_list': classroom_list})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'pk', 'pk'))
def childcare_news_create(request, pk):
    if request.method == 'POST':
        childcare = get_object_or_404(Childcare, pk=pk)
        form = ChildcareNewsCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.author = request.user
            obj.childcare = childcare
            obj.save
            form.save(commit=True)
            return HttpResponseRedirect('/childcare/%s' % pk)
    else:
        form = ChildcareNewsCreateForm()
    return render(request, 'childcare/childcare_news_create.html', {'form': form})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'pk', 'childcare_id'))
def childcare_news_detail(request, childcare_id, news_id):
    news = get_object_or_404(ChildcareNews, pk=news_id, childcare=childcare_id)
    return render(request, 'childcare/childcare_news_detail.html', {'news': news})


@login_required
@permission_required_or_403('childcare_view', (Childcare, 'pk', 'childcare_id'))
def classroom_create(request, childcare_id):
    if request.method == 'POST':
        childcare = get_object_or_404(Childcare, pk=childcare_id)
        form = ClassroomCreateForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.childcare = childcare
            teachers = form.cleaned_data['teachers']
            obj.save()
            form.save(commit=True)
            for teacher in teachers:
                assign_perm('classroom_view', teacher, childcare)
            return HttpResponseRedirect('/childcare/%s' % childcare_id)
    else:
        form = ClassroomCreateForm()
    return render(request, 'childcare/classroom_create.html', {'form': form})


@login_required
@permission_required_or_403('classroom_view', (Childcare, 'pk', 'childcare_id'))
def classroom(request, childcare_id, classroom_id):
    classroom = get_object_or_404(Classroom, pk=classroom_id)
    return render(request, 'childcare/classroom_detail.html', {'classroom': classroom})