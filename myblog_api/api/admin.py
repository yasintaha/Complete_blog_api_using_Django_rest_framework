from django.contrib import admin
from api.models import PostModel,CommentModel

# Register your models here.
admin.site.register(PostModel)
admin.site.register(CommentModel)