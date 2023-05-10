from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, authenticate, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.views.decorators.http import require_POST
from django.utils import timezone
from .models import Note
from .forms import NoteForm


def signup(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=raw_password)
            login(request, user)
            return redirect('note_list')
    else:
        form = UserCreationForm()
    return render(request, 'registration/signup.html', {'form': form})


def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('note_list')
        else:
            error_message = 'Invalid login credentials'
            return render(request, 'registration/login.html', {'error_message': error_message})
    else:
        return render(request, 'registration/login.html')


@login_required
def note_list(request):
    user = request.user
    notes = Note.objects.filter(author=user)
    shared_notes = Note.objects.filter(shared_with=user)
    return render(request, 'notes/note_list.html', {'notes': notes, 'shared_notes': shared_notes})


@login_required
def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'notes/note_detail.html', {'note': note})


@login_required
def note_new(request):
    if request.method == "POST":
        form = NoteForm(request.POST)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.created_date = timezone.now()
            note.save()
            form.save_m2m()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm()
    return render(request, 'notes/note_new.html', {'form': form})


@login_required
def note_edit(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        form = NoteForm(request.POST, instance=note)
        if form.is_valid():
            note = form.save(commit=False)
            note.author = request.user
            note.created_date = timezone.now()
            note.save()
            form.save_m2m()
            return redirect('note_detail', pk=note.pk)
    else:
        form = NoteForm(instance=note)
    return render(request, 'notes/note_edit.html', {'form': form,
                                                    'note': note})


@login_required
def note_share(request, pk):
    note = get_object_or_404(Note, pk=pk)
    if request.method == "POST":
        username = request.POST.get('username')
        user = get_object_or_404(User, username=username)
        note.shared_with.add(user)
        note.save()
        return redirect('note_detail', pk=note.pk)
    else:
        return render(request, 'notes/note_share.html', {'note': note})


@login_required
def note_delete(request, pk):
    note = get_object_or_404(Note, pk=pk)

    # Only the note owner can delete the note
    if note.author != request.user:
        messages.error(request, 'You are not authorized to delete this note.')
        return redirect('note_detail', pk=note.pk)

    if request.method == 'POST':
        note.delete()
        messages.success(request, 'The note has been deleted.')
        return redirect('note_list')

    context = {'note': note}
    return render(request, 'notes/note_delete.html', context)