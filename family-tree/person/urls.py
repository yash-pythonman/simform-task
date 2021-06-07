from django.urls import path
from rest_framework.authtoken.views import obtain_auth_token

from .views import FamilyListView, LogoutView, PersonDetailView, PersonListView

urlpatterns = [
    path("login/", obtain_auth_token, name="login"),
    path("logout/", LogoutView.as_view(), name="logout"),
    path("families/", FamilyListView.as_view(), name="family_list"),
    path("person/<int:family_id>/", PersonListView.as_view(), name="person_list"),
    path("person/<int:person_id>/", PersonDetailView.as_view(), name="person_detail"),
]
