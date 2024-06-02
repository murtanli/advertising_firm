from django.contrib import admin
from .models import Level, Profile, Employee, Service, Order, OrderDetail, Review

@admin.register(Level)
class LevelAdmin(admin.ModelAdmin):
    list_display = ('LevelID', 'LevelName', 'Discount')

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'FullName', 'Address', 'LevelID')

@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('EmployeeID', 'FullName', 'Role')

@admin.register(Service)
class ServiceAdmin(admin.ModelAdmin):
    list_display = ('ServiceID', 'ServiceName', 'Description', 'Price')

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('OrderID', 'UserID', 'Description', 'OrderDate', 'Status', 'TotalAmount')

@admin.register(OrderDetail)
class OrderDetailAdmin(admin.ModelAdmin):
    list_display = ('OrderDetailID', 'OrderID', 'ServiceID', 'Price', 'Discount')

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ('ReviewID', 'UserID', 'ServiceID', 'Rating', 'Comment')
