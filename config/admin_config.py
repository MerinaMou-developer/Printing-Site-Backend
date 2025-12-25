"""
Django Admin Site Configuration
Customize the admin site header, title, and index title
"""
from django.contrib import admin

# Customize admin site header
admin.site.site_header = "PrintPro Administration"
admin.site.site_title = "PrintPro Admin"
admin.site.index_title = "Welcome to PrintPro Administration"

