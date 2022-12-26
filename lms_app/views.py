from django.shortcuts import render , redirect , get_object_or_404
from .models import *
from .forms import BookForm, CategoryForm
# Create your views here.


def index(request):
    if request.method == 'POST':
        addBook = BookForm(request.POST, request.FILES)
        if addBook.is_valid():
            addBook.save()
        
        addCat= CategoryForm(request.POST)
        if addCat.is_valid():
            addCat.save()
            
        
    totalbooksold=0
    for i in Book.objects.values('status','price'):
        if i['status']=='sold':
            if i['price'] != None:
                totalbooksold += int(i['price'])
    #-------
    totalbookrental = 0
    for i in Book.objects.values('status', 'total_rental'):
        if i['status'] == 'rental':
            if i['total_rental'] != None:
                totalbookrental += int(i['total_rental'])
    # -------
    fullprofits = totalbooksold + totalbookrental
    context = {
        'totalbooksold': totalbooksold,
        'totalbookrental': totalbookrental,
        'fullprofits': fullprofits,
        'category': Category.objects.all(),
        'books': Book.objects.all(),
        'form': BookForm(),
        'formCat': CategoryForm(),
        'allbooks':Book.objects.filter(active=True).count(),
        'booksold': Book.objects.filter(status='sold').count(),
        'bookrental': Book.objects.filter(status='rental').count(),
        'bookavailable': Book.objects.filter(status='available').count(),
    }
    return render(request, 'pages/index.html', context)


def books(request):
    books = Book.objects.all()
    if request.method =='POST':
        addCat = CategoryForm(request.POST)
        if addCat.is_valid():
            addCat.save()
        
        if 'search_name' in request.POST:
            search = request.POST['search_name']
            if search:
                books = books.filter(title__icontains=search)
            
       
    context = {
        'category': Category.objects.all(),
        'books':  books,
        'formCat': CategoryForm()
    }
    return render(request, 'pages/books.html', context)


def update(request,id):
    book_id= Book.objects.get(id=id)
    if request.method == 'POST':
        book_update= BookForm(request.POST,request.FILES,instance=book_id)
        if book_update.is_valid():
            book_update.save()
            return redirect('/')
    
    
    context = {
        
        'form': BookForm(instance=book_id),
    }
        
    return render(request, 'pages/update.html', context)


def delete(request,id):
    book_delete =get_object_or_404(Book,id=id)
    if request.method== 'POST':
        book_delete.delete()
        return redirect('/')
    return render(request,'pages/delete.html')
