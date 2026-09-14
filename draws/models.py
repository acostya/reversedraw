from django.db import models
from django.utils.text import slugify


class Event(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=220, unique=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["-created_at"]

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)[:200] or "event"
            slug = base_slug
            n = 1
            while Event.objects.filter(slug=slug).exclude(pk=self.pk).exists():
                n += 1
                slug = f"{base_slug}-{n}"
            self.slug = slug
        super().save(*args, **kwargs)

    @property
    def called_numbers(self):
        return self.calls.order_by("position")

    @property
    def called_count(self):
        return self.calls.count()

    @property
    def latest_call(self):
        return self.calls.order_by("-position").first()


class CalledNumber(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE, related_name="calls")
    number = models.CharField(max_length=20)
    position = models.PositiveIntegerField()
    called_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ["position"]
        constraints = [
            models.UniqueConstraint(fields=["event", "position"], name="unique_call_position_per_event"),
            models.UniqueConstraint(fields=["event", "number"], name="unique_number_per_event"),
        ]

    def __str__(self):
        return f"{self.event} — {self.number}"
