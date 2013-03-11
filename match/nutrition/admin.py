from django.contrib import admin
from nutrition.models import CounselingSession, CounselingReferralState, \
    CounselingSessionState, DiscussionTopic

admin.site.register(DiscussionTopic)
admin.site.register(CounselingSession)
admin.site.register(CounselingSessionState)
admin.site.register(CounselingReferralState)
