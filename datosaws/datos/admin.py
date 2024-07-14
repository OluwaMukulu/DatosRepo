from django.contrib import admin
from .models import Address,Category,Item,Supplier,Expense,Income


# Register your models here.
admin.site.site_header = 'datos Management Information System'
admin.site.site_title = 'dastos Site Admin'
admin.site.index_title = 'datos Administration'


class AddressAdmin(admin.ModelAdmin):
    list_display = ('address_area', 'city', 'province','country')
    search_fields = ['address_area']
    list_filter = ('city','province','country')

class SupplierAdmin(admin.ModelAdmin):
    list_display = ('supplier_id', 'company_name', 'contact_name', 'phone', 'email', 'address_area')
    search_fields = ['company_name','address_area']
    list_filter = ('company_name',)

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'category_type', 'short_description')
    search_fields = ['category_type','category_name']
    list_filter = ('category_type',)

class ItemAdmin(admin.ModelAdmin):
    list_display = ('item_photo', 'name', 'short_description', 'price', 'quantity','product_type', 'company_name','total_value')
    search_fields = ['name','product_type','company_name']
    list_filter = ('product_type',)
    readonly_fields = ('item_photo',)

class ExpenseAdmin(admin.ModelAdmin):
    list_display = ('user','name','short_description','category_name', 'date', 'amount', 'payment_method')
    search_fields = ['name','company_name','category_name']
    list_filter = ('date','category_name','payment_method')

class IncomeAdmin(admin.ModelAdmin):
    list_display = ('user','name','short_description','category_name', 'date', 'amount', 'payment_method')
    search_fields = ['name','company_name','category_name']
    list_filter = ('date','category_name','payment_method')




admin.site.register(Address, AddressAdmin)
admin.site.register(Supplier, SupplierAdmin)
admin.site.register(Category, CategoryAdmin)
admin.site.register(Item, ItemAdmin)
admin.site.register(Expense, ExpenseAdmin)
admin.site.register(Income, IncomeAdmin)

