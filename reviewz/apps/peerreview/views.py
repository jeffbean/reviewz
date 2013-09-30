# Create your views here.
from django.views.generic import TemplateView, ListView, CreateView, UpdateView
from reviewz.apps.peerreview.forms import ReviewQuestionAnswerForm
from reviewz.apps.peerreview.models import PeerReview, ReviewAnswer


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


class DoReviewView( CreateView):
    form_class = ReviewQuestionAnswerForm
    template_name = 'do_review.html'
    success_url = '/myreviews/'
    context_object_name = 'review'

    def get_object(self, queryset=None):
        return ReviewAnswer.objects.get(question=self.kwargs.get('review_id'))

