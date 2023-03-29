import requests
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView
from rest_framework.decorators import permission_classes, api_view
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.response import Response

from .forms import BookForm, ReviewForm
from .models import Libro


def create_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST)
        if form.is_valid():
            book = form.save()
            return redirect('book_detail', pk=book.pk)  # Redirigir al usuario a detalles del libro
    else:
        form = BookForm()
    return render(request, 'create_book.html', {'form': form})


def book_detail(request, pk):
    book = get_object_or_404(Libro, pk=pk)
    return render(request, 'book_detail.html', {'book': book})


from django.shortcuts import render, redirect


def create_review(request, pk):
    book = get_object_or_404(Libro, id=pk)

    # lo mismo que book = Libro.objects.get(id=pk) pero con control de fallos si no lo encuentra.
    if request.method == 'POST':
        form = ReviewForm(request.POST)
        if form.is_valid():
            review = form.save(commit=False)
            review.book = book
            review.user = request.user
            review.save()
            return redirect('book_detail', pk=book.id)
    else:
        form = ReviewForm()
    return render(request, 'create_review.html', {'form': form, 'book': book})


class BookListView(ListView):
    model = Libro
    template_name = 'book_list.html'
    context_object_name = 'books'


###VISTAS API
from rest_framework import generics, status
from .serializers import LibroSerializer
from .models import Libro


@api_view(['GET'])
@permission_classes([AllowAny])
def summary(request):
    respostafinal = {'urlAPI': [
        request.build_absolute_uri() + 'simpletoken/',
        request.build_absolute_uri() + 'librolist/'
    ]}

    return Response(respostafinal)


@api_view(['POST'])
@permission_classes([AllowAny])
def addlibro(request):
    id = ''
    ntitle = request.data['title']
    nauthor = request.data['author']
    ngenre = request.data['genre']
    npages = request.data['pages']

    try:
        id = request.data['id']
    except Exception as e:
        pass

    if id == '':
        llibrenou, created = Libro.objects.get_or_create(title=ntitle, author=nauthor, genre=ngenre, pages=npages)
        if created:
            respostafinal = {'added': llibrenou.id}
        else:
            respostafinal = {'error': 'Entity exist'}
    else:
        librovell = Libro.objects.filter(pk=id).get()
        librovell.title = ntitle
        librovell.author = nauthor
        librovell.genre = ngenre
        librovell.pages = npages
        librovell.save()
        respostafinal = {'modified': librovell.id}

    return Response(respostafinal)


# @permission_classes([IsAuthenticated])
class APILibroList(generics.ListCreateAPIView):
    queryset = Libro.objects.all()
    serializer_class = LibroSerializer


@api_view(['POST'])
@permission_classes([AllowAny])
def modifylibro(request, pk):
    respostafinal = ''

    libro2change = Libro.objects.filter(pk=pk)
    if len(libro2change) == 0:
        respostafinal = 'Entrada no existe'
    else:
        libro2change = libro2change.get()
        for k, v in request.data.items():
            setattr(libro2change, k, v)
        libro2change.save()
        respostafinal = 'Modified'

    return Response(respostafinal)


@api_view(['POST'])
@permission_classes([AllowAny])
def simpletoken(request):
    """
    Gets tokens with username and password. Input should be in the format:
    {"username": "username", "password": "1234abcd"}
    """
    r = requests.post(
        'http://127.0.0.1:8000/o/token/',
        data={
            'grant_type': 'password',
            'username': request.data['username'],
            'password': request.data['password'],
            'client_id': 'LtWrSht5h6jLPeOi8rU8mEgJuRXqqqeuVijmo0Z4',
            'client_secret': 'r6vZDljavMLxQ4POhjMUbZb4DHVh4kmywDeRo7ZOsnscA1mjd2XUfStPBlLVmHPhCr7QG6clEuz3nIJI1LKo4TqIMPquWCcHfA9c0JGwwWyaXPhLFJBigbaeF6k5LxUq',
        },
    )
    dict = r.json()
    return Response(dict)
