from django.contrib.auth import get_user_model
from django.db import models

# Create your models here.


class ReviewQuestionnaire(models.Model):
    created_by = models.ForeignKey(get_user_model())
    date_created = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.title


class ReviewQuestion(models.Model):
    questionnaire = models.ManyToManyField(ReviewQuestionnaire)
    question = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return self.question


class PeerReview(models.Model):
    questionnaire = models.ForeignKey(ReviewQuestionnaire)
    from_user = models.ForeignKey(get_user_model(), related_name='from_user')
    to_user = models.ForeignKey(get_user_model(), related_name='to_user')
    is_final = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)
    date_required = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return '{0} -> {1}: {2}'.format(self.from_user, self.to_user, self.questionnaire)

    class Meta:
        unique_together = ("questionnaire", "to_user", "from_user")


class ReviewAnswer(models.Model):
    peer_review = models.ForeignKey(PeerReview)
    question = models.ForeignKey(ReviewQuestion)
    answer = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return 'Review {0}, Q: {1} A: {2}'.format(self.peer_review.to_user, self.question, self.answer)

    class Meta:
        unique_together = ('peer_review', 'question')