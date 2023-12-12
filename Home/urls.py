from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path("", views.home, name="home"),
    path("login/", views.login_page, name="login_page"),
    path("logout/", views.logout_page, name="logout"),
    path("signup/", views.signup_page, name="signup_page"),
    path("user/", views.details_page, name="details"),
    path("userprofile/", views.userprofile, name="user_profile"),
    path("profile/", views.profile, name="profile"),
    path("useredit/", views.userprofile, name="user_edit"),
    path("journal/", views.journal_entry, name="journalentry"),
    path("journalentries/", views.get_journal_entries, name="journalentries"),
    path("publicblog/", views.get_public_journal_entries, name="public"),

]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL,
                          document_root=settings.MEDIA_ROOT)
