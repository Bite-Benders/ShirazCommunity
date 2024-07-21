from django.contrib import admin
from import_export.admin import ImportExportActionModelAdmin
from group.models import Group, UserCategory


@admin.register(Group)
class GroupAdmin(ImportExportActionModelAdmin):
    list_display = ['title', 'created', 'is_active']
    list_filter = ['created', 'is_active']
    search_fields = ['title', 'chat_id']

@admin.register(UserCategory)
class UserCategoryAdmin(ImportExportActionModelAdmin):
    list_display = ['category_name', 'group']
    list_filter = ['group']


