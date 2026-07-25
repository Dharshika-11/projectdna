from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, UserProfile, Department

@admin.register(Department)
class DepartmentAdmin(admin.ModelAdmin):
    list_display = ('name', 'code', 'created_at')
    search_fields = ('name', 'code')

class UserProfileInline(admin.StackedInline):
    model = UserProfile
    can_delete = False
    verbose_name_plural = 'Profile Info'

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    inlines = (UserProfileInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'role', 'department', 'is_staff')
    list_filter = ('role', 'department', 'is_staff', 'is_superuser', 'is_active')
    fieldsets = UserAdmin.fieldsets + (
        ('PROJECTDNA RBAC', {'fields': ('role', 'department', 'roll_number', 'phone_number', 'avatar', 'designation')}),
    )
    add_fieldsets = UserAdmin.add_fieldsets + (
        ('PROJECTDNA RBAC', {'fields': ('role', 'department', 'roll_number', 'phone_number', 'avatar', 'designation')}),
    )

admin.site.register(UserProfile)
