from django.conf.urls import url, include
from django.views.generic import TemplateView
from . import views


ng_urlpatterns = [

    # Partials
    # Requested by angular-ui-router's 'templateUrl'

    # Components
    url(r'^header/$', TemplateView.as_view(template_name='components/header.html'), name='header'),
    url(r'^footer/$', TemplateView.as_view(template_name='components/footer.html'), name='footer'),

    url(r'^home/$', views.HomePartialView.as_view(), name='home'),
    url(r'^about/$', views.AboutPartialView.as_view(), name='about'),
    url(r'^maps/$', views.MapsPartialView.as_view(), name='maps'),
    url(r'^news/$', views.NewsPartialView.as_view(), name='news'),
    url(r'^services/$', views.ServicesPartialView.as_view(), name='services'),
    url(r'^projects/$', views.ProjectsPartialView.as_view(), name='projects'),

    # Do not depend on ui-router
    url(r'^modal/$', views.NgModalView.as_view(), name='ng-modal'),
]


urlpatterns = [

    # Single page views
    url(r'^$', views.OnePageAppView.as_view(), name='single-page'),

    # AngularJS views
    url(r'^', include(ng_urlpatterns)),
]