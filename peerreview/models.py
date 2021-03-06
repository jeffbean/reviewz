# coding=utf-8
from django.conf import settings
from django.core.urlresolvers import reverse
from django.db import models

# Create your models here.


class ReviewQuestionnaire(models.Model):
    created_by = models.ForeignKey(settings.AUTH_USER_MODEL)
    date_created = models.DateField(auto_now_add=True)
    title = models.CharField(max_length=255)
    description = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('questionnaire_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return self.title

    def __str__(self):
        return self.title


class ReviewQuestion(models.Model):
    questionnaire = models.ManyToManyField(ReviewQuestionnaire)
    question = models.CharField(max_length=255, unique=True)
    description = models.TextField(null=True, blank=True)

    def get_absolute_url(self):
        return reverse('question_detail', kwargs={'pk': self.pk})

    def __unicode__(self):
        return '{0}'.format(self.question)


class PeerReview(models.Model):
    questionnaire = models.ForeignKey(ReviewQuestionnaire)
    from_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='from_user')
    to_user = models.ForeignKey(settings.AUTH_USER_MODEL, related_name='to_user')
    is_final = models.BooleanField(default=False)
    date_completed = models.DateTimeField(null=True, blank=True)
    date_required = models.DateTimeField(null=True, blank=True)

    def __unicode__(self):
        return '{id}: {0} -> {1}: {2}'.format(self.from_user, self.to_user, self.questionnaire, id=self.id)

    class Meta:
        unique_together = ("questionnaire", "to_user", "from_user")


class ReviewAnswer(models.Model):
    peer_review = models.ForeignKey(PeerReview)
    question = models.ForeignKey(ReviewQuestion)
    answer = models.TextField(null=True, blank=True)

    def __unicode__(self):
        return 'A: {0}'.format(self.answer)

    class Meta:
        unique_together = ('peer_review', 'question')