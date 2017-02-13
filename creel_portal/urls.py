from django.conf.urls import url


from . import views

prj_cd_regex = r'(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})'

urlpatterns = [
    url(r'^$', views.CreelListView.as_view(),
        name='creel_list',),

    url(r'^$', views.CreelListView.as_view(),
        name='home',),

#    url((r'^creel_detail/' + prj_cd_regex + r'/$'),
#        views.CreelDetailView.as_view(),
#        name="creel_detail"),

    url(r'creel_detail/(?P<slug>[A-Za-z]{3}_[A-Za-z]{2}\d{2}_([A-Za-z]|\d){3})/$',
        views.CreelDetailView.as_view(),
        name="creel_detail"),


]
