from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from django.contrib import messages
from django.utils import timezone
from django.http import JsonResponse
from django.forms import formset_factory
from .models import *
from .forms import *

def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.category = form.cleaned_data['category']
            user.save()
            login(request, user)
            messages.success(request, 'Registration successful!')
            return redirect('home')
    else:
        form = UserRegistrationForm()
    return render(request, 'auth/register.html', {'form': form})

@login_required
def create_poll(request):
    OptionFormSet = formset_factory(OptionForm, extra=4, min_num=2, validate_min=True)
    
    if request.method == 'POST':
        poll_form = PollForm(request.POST)
        option_formset = OptionFormSet(request.POST)
        
        if poll_form.is_valid() and option_formset.is_valid():
            poll = poll_form.save(commit=False)
            poll.creator = request.user
            poll.save()
            
            for option_form in option_formset:
                if option_form.cleaned_data.get('text'):
                    Option.objects.create(
                        poll=poll,
                        text=option_form.cleaned_data['text']
                    )
            
            messages.success(request, 'Poll created successfully!')
            return redirect('poll_detail', pk=poll.pk)
    else:
        poll_form = PollForm()
        option_formset = OptionFormSet()
    
    return render(request, 'polls/create_poll.html', {
        'poll_form': poll_form,
        'option_formset': option_formset
    })

@login_required
def poll_list(request):
    # Get all active polls
    polls = Poll.objects.all().order_by('-created_at')
    
    context = {
        'polls': polls,
        'user_polls': Poll.objects.filter(creator=request.user),
        'available_polls': Poll.objects.exclude(creator=request.user)
    }
    return render(request, 'polls/poll_list.html', context)

@login_required
def poll_detail(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    user_vote = Vote.objects.filter(user=request.user, poll=poll).first()
    
    # Handle voting
    if request.method == 'POST' and not user_vote:
        option_id = request.POST.get('option')
        if option_id:
            try:
                option = Option.objects.get(pk=option_id, poll=poll)
                Vote.objects.create(
                    user=request.user,
                    poll=poll,
                    option=option
                )
                messages.success(request, 'Your vote has been recorded!')
                return redirect('poll_detail', pk=pk)
            except Option.DoesNotExist:
                messages.error(request, 'Invalid option selected.')
    
    # Calculate results
    total_votes = Vote.objects.filter(poll=poll).count()
    results = []
    
    for option in poll.options.all():
        vote_count = Vote.objects.filter(poll=poll, option=option).count()
        percentage = (vote_count / total_votes * 100) if total_votes > 0 else 0
        results.append({
            'option': option,
            'votes': vote_count,
            'percentage': round(percentage, 1)
        })
    
    context = {
        'poll': poll,
        'results': results,
        'user_vote': user_vote,
        'total_votes': total_votes,
        'can_vote': not user_vote and request.user.is_authenticated
    }
    
    return render(request, 'polls/poll_detail.html', context)

@login_required
def poll_delete(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.user == poll.creator or request.user.is_admin:
        poll.delete()
        messages.success(request, 'Poll deleted successfully!')
    return redirect('poll_list') 

@login_required
def profile(request):
    try:
        # Get user's polls with vote count
        user_polls = Poll.objects.filter(creator=request.user).prefetch_related('vote_set')
        
        # Get user's votes with related poll and option
        user_votes = Vote.objects.filter(user=request.user).select_related('poll', 'option')
        
        # Calculate totals
        total_polls = user_polls.count()
        total_votes_cast = user_votes.count()
        total_votes_received = sum(poll.vote_set.count() for poll in user_polls)
        
        context = {
            'user_polls': user_polls,
            'user_votes': user_votes,
            'total_polls': total_polls,
            'total_votes_cast': total_votes_cast,
            'total_votes_received': total_votes_received,
        }
        
        print("Debug - User:", request.user.username)
        print("Debug - Total Polls:", total_polls)
        print("Debug - Total Votes Cast:", total_votes_cast)
        
        return render(request, 'polls/profile.html', context)
        
    except Exception as e:
        print("Debug - Error:", str(e))
        return render(request, 'polls/profile.html', {'error': str(e)})

@login_required
def add_comment(request, pk):
    poll = get_object_or_404(Poll, pk=pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.user = request.user
            comment.poll = poll
            comment.save()
            messages.success(request, 'Comment added successfully!')
    return redirect('poll_detail', pk=pk) 

def home(request):
    latest_polls = []
    if request.user.is_authenticated:
        latest_polls = Poll.objects.filter(
            end_time__gte=timezone.now(),
            start_time__lte=timezone.now(),
            is_public=True
        ).order_by('-created_at')[:6]  # Show 6 latest polls
    
    return render(request, 'polls/home.html', {
        'latest_polls': latest_polls
    })

def logout_view(request):
    logout(request)
    return redirect('home')