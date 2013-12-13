# coding=utf-8
from django.contrib import admin
from django.contrib.auth.decorators import login_required
from reviewz.apps.peerreview.views import *

admin.autodiscover()
from django.conf.urls import patterns, url

urlpatterns = patterns(
    '',
    url(r'^$', PeerReviewHome.as_view(), name='home'),
    url(r'^review/(?P<pk>\d+)/$', login_required(PeerReviewView.as_view()),
        name='review'),
    url(r'^myreviews/$', login_required(MyPeerReviews.as_view()),
        name='my_reviews'),
    url(r'^do_review/(?P<pk>\d+)/$', login_required(DoReviewView.as_view()),
        name='do_review'),


    url(r'^questionnaire/create/$', QuestionnaireCreate.as_view(),
        name='questionnaire_create'),
    url(r'^questionnaire/(?P<pk>\d+)/$', QuestionnaireDetail.as_view(),
        name='questionnaire_detail'),
    url(r'^questionnaire/list/$', QuestionnaireList.as_view(),
        name='questionnaire_list'),

    url(r'^question/create/$', QuestionCreateView.as_view(), name='question_create'),
    url(r'^question/(?P<pk>\d+)/$', QuestionDetailView.as_view(), name='question_detail'),
    url(r'^question/list/$', QuestionListView.as_view(), name='question_list'),
    url(r'^question/list/(?P<pk>\d+)/$', QuestionnaireQuestionListView.as_view(), name='questionnaire_question_list'),
    #url(r'^do_review/(?P<pk>\d+)/submit/$', login_required(ReviewSubmitView.as_view()), name='submit_review'),
)
