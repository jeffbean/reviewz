from django import forms
from peerreview.models import ReviewAnswer, PeerReview, ReviewQuestion

__author__ = 'Jeffrey'


class ReviewQuestionAnswerForm(forms.ModelForm):
    def __init__(self, review, question, *args, **kwargs):
        super(ReviewQuestionAnswerForm, self).__init__(*args, **kwargs)
        self.fields['peer_review'] = forms.ModelChoiceField(queryset=PeerReview.objects.all(), initial=review)
        self.fields['question'] = forms.ModelChoiceField(queryset=ReviewQuestion.objects.all(), initial=question)

    class Meta:
        model = ReviewAnswer
