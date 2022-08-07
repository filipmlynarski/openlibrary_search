from django.contrib import admin

from core.models import AuthorSearches, BookSearches


class CountRangeFilter(admin.SimpleListFilter):
    title = 'count range'
    parameter_name = 'count_range'

    def lookups(self, request, model_admin):
        return tuple(
            (f'{start}-{start+5}', f'searched {start}-{start+5} times')
            for start in range(0, 105, 5)
        ) + (('100+', 'searched over 100 times'),)

    def queryset(self, request, queryset):
        if value := self.value():
            if value == '100+':
                return queryset.filter(count__gte=100)
            start, end = map(int, value.split('-'))
            return queryset.filter(
                count__gte=start,
                count__lte=end,
            )
        return queryset


class AuthorSearchesAdmin(admin.ModelAdmin):
    list_filter = (CountRangeFilter, )
    list_display = ('author_key', 'author_name', 'count')


class BookSearchesAdmin(admin.ModelAdmin):
    list_filter = (CountRangeFilter, )
    list_display = ('key', 'title', 'count')


admin.site.register(AuthorSearches, AuthorSearchesAdmin)
admin.site.register(BookSearches, BookSearchesAdmin)
