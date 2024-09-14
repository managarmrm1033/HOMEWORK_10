
from django.shortcuts import render

from .forms import TagForm, NoteForm
from .models import Tag, Note

from .forms import AuthorForm

from .models import Author

from django.contrib import messages
from django.http import HttpResponseNotAllowed
from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import Note

from django.http import JsonResponse

from django.db.models import Count

from django.core.paginator import Paginator


def main(request):
    notes = Note.objects.filter(user=request.user).all() if request.user.is_authenticated else []
    authors = Author.objects.all()

    # Get top 10 tags by the number of associated notes
    top_tags = Tag.objects.annotate(num_notes=Count('note')).order_by('-num_notes')[:10]

    # Paginate notes
    paginator = Paginator(notes, 5)  # Show 10 notes per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'noteapp/index.html', {
        "notes": page_obj.object_list,
        "authors": authors,
        "top_tags": top_tags,
        "page_obj": page_obj
    })

@login_required
def tag(request):
    if request.method == 'POST':
        form = TagForm(request.POST)
        if form.is_valid():
            tag = form.save(commit=False)
            tag.user = request.user
            tag.save()
            return redirect(to='noteapp:main')
        else:
            return render(request, 'noteapp/tag.html', {'form': form})

    return render(request, 'noteapp/tag.html', {'form': TagForm()})


@login_required
def note(request):
    tags = Tag.objects.filter(user=request.user).all()

    if request.method == 'POST':
        form = NoteForm(request.POST, user=request.user)
        if form.is_valid():
            new_note = form.save(commit=False)
            new_note.user = request.user
            new_note.save()
            choice_tags = Tag.objects.filter(name__in=request.POST.getlist('tags'), user=request.user)
            for tag in choice_tags.iterator():
                new_note.tags.add(tag)
            return redirect(to='noteapp:main')
    else:
        form = NoteForm(user=request.user)

    return render(request, 'noteapp/note.html', {"tags": tags, 'form': form})

def note_list(request):
    notes = Note.objects.all()
    return render(request, 'noteapp/note_list.html', {'notes': notes})

def note_detail(request, pk):
    note = get_object_or_404(Note, pk=pk)
    return render(request, 'noteapp/note_detail.html', {'note': note})


@login_required
def detail(request, note_id):
    note = get_object_or_404(Note, pk=note_id, user=request.user)
    return render(request, 'noteapp/detail.html', {"note": note})


@login_required
def set_done(request, note_id):
    Note.objects.filter(pk=note_id, user=request.user).update(done=True)
    return redirect(to='noteapp:main')


@login_required
def delete_note(request, id):
    if request.method == 'POST':
        note = get_object_or_404(Note, id=id)
        note.delete()
        return redirect('noteapp:note_list')
    else:
        return HttpResponseNotAllowed(['POST'])
@login_required
def profile(request):
    return render(request, 'users/profile.html')

@login_required
def add_author(request):
    if request.method == 'POST':
        form = AuthorForm(request.POST)
        if form.is_valid():
            author = form.save(commit=False)
            author.user = request.user
            author.save()
            return redirect(to='noteapp:author_list')  #'author_list'
    else:
        form = AuthorForm()
    return render(request, 'noteapp/add_author.html', {'form': form})


def author_list(request):
    authors = Author.objects.all()
    return render(request, 'noteapp/author_list.html', {'authors': authors})

@login_required
def delete_author(request, author_id):
    if request.method == 'POST':
        author = get_object_or_404(Author, id=author_id)
        author.delete()
        return JsonResponse({'status': 'success'})
    return JsonResponse({'status': 'error'}, status=400)
def author_detail(request, pk):
    author = get_object_or_404(Author, pk=pk)
    return render(request, 'noteapp/authors_detail.html', {'author': author})


def tagged_notes(request, tag_name):
    tag = get_object_or_404(Tag, name=tag_name)
    notes = tag.note_set.all()

    # Пагінація для нотаток
    paginator = Paginator(notes, 5)  # 5 нотаток на сторінку
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'noteapp/tagged_notes.html', {'notes': page_obj, 'tag': tag})

def notes_by_tag(request, tag_id):
    tag = get_object_or_404(Tag, id=tag_id)
    notes = Note.objects.filter(tags=tag)

    paginator = Paginator(notes, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'noteapp/notes_by_tag.html', {'tag': tag, 'page_obj': page_obj})

