from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import TemplateView, DetailView, ListView, CreateView
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.db.models import Avg, Sum, Q
from django.urls import reverse_lazy

from .models import Resource, Rating, Report, ResourceRequest
from .filters import ResourceFilter
from django_filters.views import FilterView


class DashboardView(LoginRequiredMixin, TemplateView):
    template_name = 'resources/dashboard.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        exam = self.request.GET.get('exam')
        qs = Resource.objects.filter(is_approved=True).select_related('subject', 'uploaded_by')
        if exam:
            qs = qs.filter(Q(type='PYQ') | Q(is_important=True))
        ctx['recent'] = qs.order_by('-created_at')[:6]
        ctx['top_rated'] = qs.order_by('-avg_rating')[:5]
        ctx['my_uploads'] = Resource.objects.filter(uploaded_by=user).count()
        ctx['my_downloads'] = Resource.objects.filter(uploaded_by=user).aggregate(t=Sum('downloads'))['t'] or 0
        ctx['open_requests'] = ResourceRequest.objects.filter(is_fulfilled=False).order_by('-created_at')[:5]
        ctx['exam_mode'] = bool(exam)
        return ctx


class ResourceListView(LoginRequiredMixin, FilterView):
    model = Resource
    template_name = 'resources/resource_list.html'
    filterset_class = ResourceFilter
    paginate_by = 10
    context_object_name = 'resources'

    def get_queryset(self):
        qs = Resource.objects.filter(is_approved=True).select_related('subject', 'uploaded_by').order_by('-created_at')
        if self.request.GET.get('exam'):
            qs = qs.filter(Q(type='PYQ') | Q(is_important=True))
        return qs


class ResourceDetailView(LoginRequiredMixin, DetailView):
    model = Resource
    template_name = 'resources/resource_detail.html'

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        user = self.request.user
        ctx['user_rating'] = Rating.objects.filter(user=user, resource=self.object).first()
        ctx['related'] = Resource.objects.filter(subject=self.object.subject).exclude(pk=self.object.pk)[:4]
        return ctx


@login_required
def download_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    resource.downloads += 1
    resource.save(update_fields=['downloads'])
    uploader = resource.uploaded_by
    uploader.points += 1
    uploader.save(update_fields=['points'])
    return FileResponse(open(resource.file.path, 'rb'), as_attachment=True)


@login_required
def rate_resource(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    score = int(request.POST.get('score', 0))
    if 1 <= score <= 5:
        Rating.objects.update_or_create(
            user=request.user, resource=resource,
            defaults={'score': score}
        )
        avg = Rating.objects.filter(resource=resource).aggregate(a=Avg('score'))['a'] or 0
        resource.avg_rating = round(avg, 2)
        if resource.avg_rating >= 4.0:
            resource.uploaded_by.points += 5
            resource.uploaded_by.save(update_fields=['points'])
        resource.save(update_fields=['avg_rating'])
    return redirect('resource_detail', pk=pk)


@login_required
def toggle_important(request, pk):
    resource = get_object_or_404(Resource, pk=pk)
    resource.is_important = not resource.is_important
    resource.save(update_fields=['is_important'])
    return redirect('resource_detail', pk=pk)


@login_required
def report_resource(request, pk):
    if request.method == 'POST':
        resource = get_object_or_404(Resource, pk=pk)
        Report.objects.create(
            user=request.user,
            resource=resource,
            reason=request.POST.get('reason', '')
        )
    return redirect('resource_detail', pk=pk)


class RequestListView(LoginRequiredMixin, ListView):
    model = ResourceRequest
    template_name = 'resources/request_list.html'
    context_object_name = 'requests'
    queryset = ResourceRequest.objects.filter(is_fulfilled=False).order_by('-created_at')


class RequestCreateView(LoginRequiredMixin, CreateView):
    model = ResourceRequest
    fields = ['subject', 'description']
    template_name = 'resources/request_form.html'
    success_url = reverse_lazy('requests')

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)