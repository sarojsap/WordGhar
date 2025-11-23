import re
import threading
from django.db import models
from django.conf import settings
from django.utils import timezone
from django.db.models.signals import post_save
from django.dispatch import receiver
from .ai_utils import generate_summary

class WritingCategory(models.TextChoices):
    POEM = "poem", "Poem"
    STORY = "story", "Story"

class Writing(models.Model):
    # Professional Fix: Use settings.AUTH_USER_MODEL
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='writings'
    )
    title = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=WritingCategory.choices)
    slug = models.SlugField(max_length=255, unique=True, allow_unicode=True, blank=True)
    content = models.TextField()

    # AI-generated summary
    summary = models.TextField(blank=True, null=True)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Writing"
        verbose_name_plural = "Writings"

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = self.generate_nepali_slug(self.title)
        super().save(*args, **kwargs)

    def generate_nepali_slug(self, text):
        text = text.strip()
        text = re.sub(r'\s+', '-', text)
        text = re.sub(r'[.,"\';:?!(){}\[\]<>|/\\@#$%^&*~`]', '', text)
        return text

    def __str__(self):
        return f"{self.title} ({self.category})"
    

def run_ai_summary_background(writing_id, content):
    """
    This function runs in a separate thread.
    It performs the slow API call and updates the DB.
    """
    print(f"Starting background AI task for Writing ID: {writing_id}")
    summary_text = generate_summary(content)
    
    if summary_text:
        # We assume 'Writing' is imported or available. 
        # Since this is in models.py, we can access the class directly.
        Writing.objects.filter(pk=writing_id).update(summary=summary_text)
        print(f"AI Summary updated for Writing ID: {writing_id}")
    else:
        print(f"AI Summary failed for Writing ID: {writing_id}")

@receiver(post_save, sender=Writing)
def generate_summary_signal(sender, instance, created, **kwargs):
    """
    Trigger AI summarization in a background thread.
    """
    # Only run on create, and only if summary is empty
    if created and not instance.summary:
        # Create a thread that targets our helper function
        task_thread = threading.Thread(
            target=run_ai_summary_background,
            args=(instance.pk, instance.content)
        )
        # Daemon=True means the thread will die if the main server process dies (good for safety)
        task_thread.daemon = True
        task_thread.start()