from django.contrib.admin import AdminSite

class Comment8orAdminSite(AdminSite):
    title_header = 'Comment8or Admin'
    site_header = 'Comment8or administration'
    index_title = 'Comment8or site admin'
    logout_template = 'comment8or/logged_out.html'