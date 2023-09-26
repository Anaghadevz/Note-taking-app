from django.shortcuts import redirect, render
from . forms import *  
from django.contrib import messages
from django.views import generic
from django.contrib.auth.decorators import login_required

# Create your views here.
def home(request):
    return render(request,'mynotes/home.html')

@login_required

def notes(request):
    if request.method == "POST":
        form = NotesForm(request.POST)
        if form.is_valid():
             notes = Notes(user=request.user,title=request.POST['title'],description=request.POST['description'])
             notes.save()
        messages.success(request,f"Notes Added from {request.user.username} Successfully!")
    
    else:    
        form = NotesForm()
    notes=Notes.objects.filter(user=request.user)
    context={'notes':notes,'form':form}
    return render(request,'mynotes/notes.html',context)

@login_required
def delete_note(request,pk=None):
    Notes.objects.get(id=pk).delete()
    return redirect("notes")


class NotesDetailView(generic.DetailView):
    model = Notes

def register(request):
    if request.method == 'POST':
        form = UserRegistraionForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request,f"Account Created for {username}!!")
            return redirect("login")
    else:
       form = UserRegistraionForm()
    context = {
        'form':form
    }
    return render(request,"mynotes/register.html",context)

def profile(request):
    return render(request,"mynotes/profile.html")

