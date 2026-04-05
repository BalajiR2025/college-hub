from django.shortcuts import render
from django.views.generic import ListView
from django.contrib.auth.mixins import LoginRequiredMixin
from accounts.models import Student
from django.utils import timezone
import datetime

class LeaderboardView(LoginRequiredMixin, ListView):
    template_name = 'leaderboard/leaderboard.html'
    context_object_name = 'top_students'
    paginate_by = 10

    def get_queryset(self):
        return Student.objects.filter(is_approved=True).order_by('-points')[:10]
