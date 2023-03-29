from django.contrib import admin

from library.models import Libro, Review


class LibroAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'genre', 'pages')
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('book', 'user', 'content', 'score')

admin.site.register(Libro, LibroAdmin)
admin.site.register(Review, ReviewAdmin)
