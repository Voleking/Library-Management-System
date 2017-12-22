from django.contrib import admin
from datetime import date
from django.utils.translation import gettext_lazy as _
from .models import *

class OverdueFilter(admin.SimpleListFilter):
    title = _('Date')
    parameter_name = 'rc'

    def lookups(self, request, model_admin):
        return (
            ('overdue', _('Overdue')),
        )

    def queryset(self, request, queryset):
        if self.value() == 'overdue':
            return queryset.filter(is_returned=False, date_return__lt=date.today())

class BookAdmin(admin.ModelAdmin):
    list_display = ('name', 'author', 'publishing', 'category')
    search_fields = ['name', 'author', 'publishing', 'category']

class ProfileAdmin(admin.ModelAdmin):
    list_display = ('get_username', 'sex', 'level')
    search_fields = ['user__username']
    def get_username(self, instance):
        return instance.user.username
    get_username.short_description = 'Reader'

class BorrowAdmin(admin.ModelAdmin):
    list_display = ('get_reader', 'get_book', 'date_borrow', 'date_return', 'is_returned', 'is_lost')
    search_fields = ['reader__user__username', 'book__name']
    list_filter = (OverdueFilter, )
    actions = ['make_returned', 'make_lost']

    def get_reader(self, instance):
        return instance.reader.user.username
    get_reader.short_description = 'Reader'
    def get_book(self, instance):

        return instance.book.name
    get_book.short_description = 'Book'

    def suit_row_attributes(self, obj, request):
        if obj.date_return < date.today() and not obj.is_returned:
            return {'class': 'table-danger'}
        if obj.is_lost:
            return {'class': 'table-warning'}

    def make_returned(self, request, queryset):
        queryset.update(is_returned=True)
        for borrow in queryset:
            book = borrow.book
            book.quantity_out -= 1
            book.save()
    make_returned.short_description = 'Return books'

    def make_lost(self, request, queryset):
        queryset.update(is_lost=True)
        for borrow in queryset:
            book = borrow.book
            book.quantity_loss += 1
            book.quantity_out -= 1
            book.save()
    make_lost.short_description = 'Report books lost'

class MemberLevelAdmin(admin.ModelAdmin):
    list_display = ('level', 'days', 'numbers', 'fee')

class LossReportingAdmin(admin.ModelAdmin):
    list_display = ('get_reader',)
    search_fields = ['reader__user__username']
    def get_reader(self, instance):
        return instance.reader.user.username
    get_reader.short_description = 'Reader'

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Book, BookAdmin)
admin.site.register(Borrow, BorrowAdmin)
admin.site.register(BookCategory)
admin.site.register(MemberLevel, MemberLevelAdmin)
admin.site.register(LossReporting, LossReportingAdmin)
