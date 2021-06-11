from django.urls import path, include, re_path

from django.contrib import admin
from django.contrib.auth import views as auth_views
from django.conf import settings
from django.conf.urls.static import static
from django.views.i18n import JavaScriptCatalog

admin.autodiscover()

import hello.views
import hello.admin_form

# To add a new path, first import the app:
# import blog
#
# Then add the new path:
# path('blog/', blog.urls, name="blog")
#
# Learn more here: https://docs.djangoproject.com/en/2.1/topics/http/urls/

urlpatterns = [
    path("", hello.views.index, name="index"),
    # old, not efficient:
    # path("dieinstantly", bruh.die, name = "youded"),
    # path("dieinstantly2", bruh.die2, name = "youdeder"),
    path("db/", hello.views.db, name="db"),
    path("admin/", admin.site.urls, name = "admin"),
    path("register/", hello.views.register, name="register"),
    path("login/", auth_views.LoginView.as_view(template_name ="login.html"), name = "login"),
    path("logout/", auth_views.LogoutView.as_view(template_name ="logout.html"), name = "logout"),

    path("search_room", hello.views.search_room, name="search_room"),
    path("get_upcoming", hello.views.get_upcoming, name="get_upcoming"),
    path("book_room", hello.views.book_room, name="book_room"),
    path("cancel_book", hello.views.cancel_book, name="cancel_book"),

    path("modify_first", hello.views.modify_first, name="modify_first"),
    path("modify_cancel", hello.views.modify_cancel, name="modify_cancel"),

    path("admin_view_room_usage/", hello.admin_form.admin_view_room_usage, name="admin_view_room_usage"),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)