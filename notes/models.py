from django.db import models


class Note(models.Model):
    title = models.CharField(max_length=200, blank=True)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title or f"Note {self.pk}"

    def display_title(self):
        if self.title:
            return self.title
        return self.content[:60] + ('…' if len(self.content) > 60 else '')
