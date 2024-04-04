from django.contrib import admin
from django.contrib.admin.apps import AdminConfig
from django.template.response import TemplateResponse
from django.urls import path

class BookrAdmin(admin.AdminSite):
    logout_template = 'admin/logout.html'
    
    title_header = 'Bookr Admin'
    site_header = 'Bookr administration'
    index_title = 'Bookr site admin'

    def get_urls(self):
        urls = super().get_urls()
        url_patterns = [
            path('admin_profile', self.admin_view(self.profile_view)),
        ]
        return url_patterns + urls

    def profile_view(self, request):
        request.current_app = self.name
        context = self.each_context(request)
        return TemplateResponse(request, 'admin/admin_profile.html', context)
    


class BookrAdminConfig(AdminConfig):
    default_site = 'bookr_admin.admin.BookrAdmin'

