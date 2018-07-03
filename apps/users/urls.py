from django.conf.urls import url

from users import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    # url(r'^register$', views.register, name="register"),
    url(r'^register$', views.RegisterView.as_view(), name="register"),
    url(r'^active/(?P<token>.+)$', views.ActiveView.as_view(), name="active"),
    url(r'^login$', views.LoginView.as_view(), name="login"),
    url(r'^logout$', views.LogoutView.as_view(), name="logout"),
    # url(r'^address$', login_required(views.AddressView.as_view()), name="address"),
    url(r'^address$', views.AddressView.as_view(), name="address"),
    url(r'^info$', views.UserInfoView.as_view(), name="info"),
]
