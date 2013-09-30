# Create your views here.
from django.core.urlresolvers import reverse
from django.db.transaction import commit_on_success
from django.http.response import HttpResponseRedirect, HttpResponseForbidden, Http404
from django.views.generic import TemplateView, ListView, CreateView
from django.views.generic.detail import SingleObjectMixin, DetailView
from reviewz.apps.peerreview.forms import ReviewQuestionAnswerForm
from reviewz.apps.peerreview.models import PeerReview, ReviewAnswer, ReviewQuestion


class PeerReviewHome(TemplateView):
    template_name = 'peer_review_home.html'


class MyPeerReviews(ListView):
    template_name = 'my_reviews.html'
    model = PeerReview
    paginate_by = 5

    def get_queryset(self):
        """
        needs to be in this method to access self for the request object.
        @return: the queryset based on the request user
        """
        return self.model.objects.filter(from_user=self.request.user)


class PeerReviewView(DetailView):
    template_name = 'review.html'
    model = PeerReview
    context_object_name = 'review'

    def get_context_data(self, **kwargs):
        context = super(PeerReviewView, self).get_context_data(**kwargs)
        questions = self.get_object().questionnaire.reviewquestion_set.filter(questionnaire=self.get_object().questionnaire)
        context['questions'] = questions
        return context


class DoReviewView(DetailView):
    template_name = 'do_review.html'

    def get_object(self, queryset=None):
        return PeerReview.objects.get(id=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        forms = []
        context = super(DoReviewView, self).get_context_data(**kwargs)
        peer_review = self.get_object()
        context['review'] = peer_review
        questions = peer_review.questionnaire.reviewquestion_set.all()
        context['questions'] = questions
        for question in questions:
            forms.append(ReviewQuestionAnswerForm(peer_review, question))
        context['forms'] = forms
        return context

    @commit_on_success()
    def post(self, request, *args, **kwargs):
        """
        <QueryDict: {u'answer': [u'Rain', u'blue', u'both answers'], u'question': [u'1', u'2', u'4'], u'peer_review': [u'1', u'1', u'1']}>
        """
        print request.POST
        if not request.user.is_authenticated():
            return HttpResponseForbidden()

        post_dict = dict(request.POST)

        for index in range(0, len((post_dict.get('question')))):
            try:
                peer_review = PeerReview.objects.get(id=post_dict['peer_review'][index])
            except PeerReview.DoesNotExist:
                raise Http404
            try:
                review_question = ReviewQuestion.objects.get(id=post_dict['question'][index])
            except ReviewQuestion.DoesNotExist:
                raise Http404

            (review_answer, created) = ReviewAnswer.objects.get_or_create(peer_review=peer_review, question=review_question)
            review_answer.answer = post_dict['answer'][index]
            review_answer.save()
            print review_answer
        return HttpResponseRedirect(reverse('review', kwargs={'pk': self.get_object().pk}))


