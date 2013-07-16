from match.main.models import GlossaryTerm, UserProfile, UserVisited
from django.contrib import admin
from match.main.models import ImageMapItem

admin.site.register(UserProfile)
admin.site.register(GlossaryTerm)
admin.site.register(ImageMapItem)


class UserVisitedAdmin(admin.ModelAdmin):
    class Meta:
        model = UserVisited

    search_fields = ["user__user__username"]
    list_display = ("user", "section", "visited_time")

admin.site.register(UserVisited, UserVisitedAdmin)
