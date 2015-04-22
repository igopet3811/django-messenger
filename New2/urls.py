from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

# import every thing
from chat_app.views import *

urlpatterns = patterns('',

    url(r'^$', home),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^login/$',login),
    url(r'^logout/$',logout),
    url(r'^register/$',register),
    url(r'^register_success/$',register_success),
    url(r'^auth/$',auth_view),
    url(r'^chatslist/$',chatslist),
    url(r'^chatroom/(?P<Chatroom_id>\d+)/$', chatroom),
    url(r'^chatroom/(?P<Chatroom_id>\d+)/addToChat/$', addToChat),
    url(r'^addMessage/(?P<Chatroom_id>\d+)/$', addMessage),
    url(r'^chatroom/(?P<Chatroom_id>\d+)/refresh/$', chatroom_refresh),
    url(r'^profile/(?P<profile_id>\d+)/$', profile),
    url(r'^profile/(?P<profile_id>\d+)/edit_profile/$', update_profile),
    url(r'^profile/(?P<profile_id>\d+)/changeImage/$', changeImage),
    url(r'^profile/(?P<profile_id>\d+)/addContact/$', addContact),
    url(r'^profile/(?P<profile_id>\d+)/createRoom/$', createRoom),
    url(r'^search/$',search),


)
