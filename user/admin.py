from django import forms
from django.contrib import admin
from django.contrib.auth.models import Group
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib.auth.forms import ReadOnlyPasswordHashField
from django.core.exceptions import ValidationError
from import_export.admin import ImportExportActionModelAdmin
from user.models import *


class UserCreationForm(forms.ModelForm):
    """A form for creating new users. Includes all the required
    fields, plus a repeated password."""

    password1 = forms.CharField(label="رمز", widget=forms.PasswordInput)
    password2 = forms.CharField(
        label="تکرار رمز", widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["user_id", "password1", "password2"]

    def clean_password2(self):
        # Check that the two password entries match
        password1 = self.cleaned_data.get("password1")
        password2 = self.cleaned_data.get("password2")
        if password1 and password2 and password1 != password2:
            raise ValidationError("رمز با تکرار رمز مطابقت ندارد")
        return password2

    def save(self, commit=True):
        # Save the provided password in hashed format
        user = super().save(commit=False)
        if not user.username:
            user.username = user.user_id
        user.set_password(self.cleaned_data["password1"])
        if commit:
            user.save()
        return user


class UserChangeForm(forms.ModelForm):
    """A form for updating users. Includes all the fields on
    the user, but replaces the password field with admin's
    disabled password hash display field.
    """

    password = ReadOnlyPasswordHashField()

    class Meta:
        model = User
        fields = ["user_id", "password"]


@admin.register(User)
class ContactAdmin(ImportExportActionModelAdmin):
    # The forms to add and change user instances
    form = UserChangeForm
    add_form = UserCreationForm

    # The fields to be used in displaying the User model.
    # These override the definitions on the base UserAdmin
    # that reference specific fields on auth.User.
    list_display = ["username", 'user_id', "is_admin", 'instagram_id', 'number']
    list_filter = ["is_admin",]
    readonly_fields = ['user_id', 'username', 'name', 'message_count']
    fieldsets = [
        ("اطلاعات کاربری", {"fields": ["real_name",'instagram_id', 'number', 'message_count']}),
        ("ایدی کاربر", {"fields": ["name", "username", 'user_id']}),
        ("دسترسی کاریر", {"fields": ["is_admin", 'is_dev',]}),
    ]
    # add_fieldsets is not a standard ModelAdmin attribute. UserAdmin
    # overrides get_fieldsets to use this attribute when creating a user.
    add_fieldsets = [
        (
            None,
            {
                "classes": ["wide"],
                "fields": ["username", "password1", "password2"],
            },
        ),
    ]
    search_fields = ["username", 'is_admin']
    ordering = ["username"]
    filter_horizontal = []
admin.site.unregister(Group)