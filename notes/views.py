from django.shortcuts import render, redirect

from .forms import NoteForm
from .models import Note


def note_list(request):
    notes = Note.objects.all()
    return render(request, 'notes/note_list.html', {'notes': notes})


def note_create(request):
    if request.method == 'POST':
        form = NoteForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('notes:list')
    else:
        form = NoteForm()

    return render(request, 'notes/note_form.html', {'form': form})
