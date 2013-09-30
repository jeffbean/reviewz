from django.contrib import admin
from django.contrib.auth.decorators import login_required
from reviewz.apps.peerreview.views import PeerReviewHome, MyPeerReviews, DoReviewView

admin.autodiscover()
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', PeerReviewHome.as_view(), name='home'),
    url(r'^myreviews/$', login_required(MyPeerReviews.as_view()), name='my_reviews'),
    url(r'^do_review/(?P<review_id>\d+)/$', login_required(DoReviewView.as_view()), name='do_review'),
)
