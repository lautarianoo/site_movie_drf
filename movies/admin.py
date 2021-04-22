from django.contrib import admin
from django import forms
from django.utils.safestring import mark_safe

from movies.models import *

from ckeditor_uploader.widgets import CKEditorUploadingWidget


class MovieAdminForm(forms.ModelForm):
    description = forms.CharField(label='Описание' ,widget=CKEditorUploadingWidget())
    class Meta:
        model = Movie
        fields = '__all__'

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    #Категории на странице админки
    list_display =  ('id', 'name', 'url', )
    list_display_links = ('name', )

class ReviewInlines(admin.StackedInline):
    #Выделение отдельных блоков в админке в разделе фильмы
    model = Review
    extra = 0

class MovieShotsInlines(admin.TabularInline):
    model = MovieShots
    extra = 0
    readonly_fields = ('get_image',)
    exclude = ['description']

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="150" height="150">')

    get_image.short_description = 'Изображение'

@admin.register(Movie)
class MovieAdmin(admin.ModelAdmin):
    #Фильмы в админке
    list_display = ('title', 'category', 'url', 'draft', 'get_poster', )
    list_filter = ('category', 'year', )
    search_fields = ('title', 'category__name', )
    inlines = [MovieShotsInlines, ReviewInlines]
    form = MovieAdminForm
    actions = ['publish', 'unpublish']

    readonly_fields = ('get_poster',)

    def get_poster(self, obj):
        return mark_safe(f'<img src={obj.poster.url} width="50" height="60">')

    def unpublish(self, request, queryset):
        '''Снять с публикации(action)'''
        row_update = queryset.update(draft=True)
        if row_update == 1:
            message_bit = '1 запис было объявлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    def publish(self, request, queryset):
        '''Опубликолвать(action)'''
        row_update = queryset.update(draft=False)
        if row_update == 1:
            message_bit = '1 запис было объявлена'
        else:
            message_bit = f'{row_update} записей были обновлены'
        self.message_user(request, f'{message_bit}')

    publish.short_description = 'Опубликовать'
    publish.allowed_permissions = ('change', )

    unpublish.short_description = 'Снять с публикации'
    unpublish.allowed_permissions = ('change', )

    get_poster.short_description = 'Постер'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    #отзывы на странице админки
    list_display = ('name', 'email', 'parent', 'movie', 'id', )

@admin.register(Genre)
class GenreAdmin(admin.ModelAdmin):
    list_display = ('name', 'url', )

@admin.register(Actor)
class ActorAdmin(admin.ModelAdmin):
    list_display = ('name', 'age', 'get_image')
    readonly_fields = ('get_image', )

    def get_image(self, obj):
        return mark_safe(f'<img src={obj.image.url} width="50" height="60">')

    get_image.short_description = 'Изображение'

@admin.register(Rating)
class RatingAdmin(admin.ModelAdmin):
    list_display = ('star', 'movie', 'ip', )

@admin.register(MovieShots)
class MovieShotsAdmin(admin.ModelAdmin):
    list_display = ('title', 'movie', )


admin.site.register(RatingStar)