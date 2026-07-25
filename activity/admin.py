from django.contrib import admin
from .models import WorkLog, DecisionLog, Task, BugReport

admin.site.register(WorkLog)
admin.site.register(DecisionLog)
admin.site.register(Task)
admin.site.register(BugReport)
