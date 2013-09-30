from django import forms
from reviewz.apps.peerreview.models import ReviewAnswer

__author__ = 'Jeffrey'


class ReviewQuestionAnswerForm(forms.ModelForm):

    class Meta:
        model = ReviewAnswer


