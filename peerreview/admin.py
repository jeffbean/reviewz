from django.contrib import admin
from peerreview.models import ReviewQuestionnaire, ReviewQuestion, PeerReview, ReviewAnswer

__author__ = 'Jeffrey'


class PeerReviewerInline(admin.TabularInline):
    model = PeerReview
    exclude = ['is_final', 'date_completed']


class ReviewQuestionnaireAdmin(admin.ModelAdmin):
    fieldsets = (
        (None, {
            'fields': ('created_by', 'title', 'description')
        }),
    )
    inlines = [
        PeerReviewerInline,
    ]


admin.site.register(ReviewQuestionnaire, ReviewQuestionnaireAdmin)
admin.site.register(PeerReview)
admin.site.register(ReviewQuestion)
admin.site.register(ReviewAnswer)

