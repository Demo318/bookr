from django.contrib import admin
from django.contrib.admin.apps import AdminConfig

class BookrAdmin(admin.AdminSite):
    site_header = "Bookr Administration"

class BookrAdminConfig(AdminConfig):
    default_site = 'bookr_admin.admin.BookrAdmin'

