import django_filters
from .models import Resource
from subjects.models import Subject

class ResourceFilter(django_filters.FilterSet):
    search = django_filters.CharFilter(method='filter_search', label='Search')
    department = django_filters.CharFilter(field_name='subject__department', label='Department')
    semester = django_filters.NumberFilter(field_name='subject__semester', label='Semester')

    def filter_search(self, qs, name, value):
        from django.db.models import Q
        return qs.filter(Q(title__icontains=value) | Q(subject__name__icontains=value))

    class Meta:
        model = Resource
        fields = ['search','department','semester','subject','type','is_important']
