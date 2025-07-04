from django.db import models
from django.utils.text import slugify

class Product(models.Model):
    name        = models.CharField(max_length=255)
    slug        = models.SlugField(max_length=255, unique=True, blank=True)
    description = models.TextField(blank=True)
    price       = models.DecimalField(max_digits=10, decimal_places=2)
    inventory   = models.PositiveIntegerField(default=0)
    image       = models.ImageField(upload_to='products/%Y/%m/%d/', blank=True, null=True)
    created_at  = models.DateTimeField(auto_now_add=True)
    updated_at  = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']
        indexes = [models.Index(fields=['slug']),]

    def save(self, *args, **kwargs):
        if not self.slug:
            # auto-generate slug on first save
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
