from django.contrib import admin

from travel.accounts.models import Profile, ProjectUser
#from project.web.admin import ReviewsInlineAdmin


@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
    #inlines = (ReviewsInlineAdmin,)
    list_display = ('first_name', 'last_name')


@admin.register(ProjectUser)
class UserAdmin(admin.ModelAdmin):
    list_display = ('username', 'last_login', 'is_superuser', 'is_staff')