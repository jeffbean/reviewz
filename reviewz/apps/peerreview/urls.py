from django.contrib import admin
from reviewz.apps.peerreview.views import PeerReviewHome, MyPeerReviews, DoReviewView

admin.autodiscover()
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', PeerReviewHome.as_view(), name='home'),
    url(r'^myreviews/$', MyPeerReviews.as_view(), name='my_reviews'),
    url(r'^do_review/(?P<review_id>\d+)/$', DoReviewView.as_view(), name='do_review'),
)
