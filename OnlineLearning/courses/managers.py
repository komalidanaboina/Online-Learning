from django.db import models


class PublishedCourseQuerySet(models.QuerySet):
    def published(self):
        return self.filter(status='published', is_active=True)

    def featured(self):
        return self.published().filter(is_featured=True)


class PublishedCourseManager(models.Manager):
    def get_queryset(self):
        return PublishedCourseQuerySet(self.model, using=self._db).published()
