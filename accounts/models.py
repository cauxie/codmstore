# accounts/models.py
from django.db import models
import random

class Account(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    screenshot = models.ImageField(upload_to="accounts/")
    available = models.BooleanField(default=True)

    def __str__(self):
        return self.name

class Review(models.Model):
    full_name = models.CharField(max_length=100)
    comment = models.TextField()
    rating = models.IntegerField()
    photo = models.ImageField(upload_to='reviews/', blank=True, null=True)
    user_type = models.CharField(max_length=50, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    color = models.CharField(max_length=20, default='purple')
    initials = models.CharField(max_length=2, blank=True)
    
    
    def save(self, *args, **kwargs):
        if not self.initials and self.full_name:
            names = self.full_name.split()
            if len(names) >= 2:
                self.initials = (names[0][0] + names[-1][0]).upper()
            else:
                self.initials = self.full_name[:2].upper()
        
        colors = ['purple', 'blue', 'green', 'red', 'indigo', 'pink', 'yellow']
        if not self.color:
            self.color = random.choice(colors)
            
        super().save(*args, **kwargs)
    
    def __str__(self):
        return f"{self.full_name} - {self.rating} stars"

from django.db import models

class Product(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sale', 'On Sale'),
        ('sold', 'Sold'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    # REMOVE these single media fields:
    # video = models.FileField(upload_to='product_videos/', blank=True, null=True)
    # image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_on_sale(self):
        return self.status == 'sale'
    
    def current_price(self):
        return self.sale_price if self.is_on_sale() else self.price
    
    def get_primary_image(self):
        """Get the first image for thumbnail purposes"""
        first_image = self.media_files.filter(image__isnull=False).first()
        return first_image.image if first_image else None
    
    def get_primary_video(self):
        """Get the first video for thumbnail purposes"""
        first_video = self.media_files.filter(video__isnull=False).first()
        return first_video.video if first_video else None
    
    def __str__(self):
        return self.name

class ProductMedia(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='media_files')
    image = models.ImageField(upload_to='product_images/', blank=True, null=True)
    video = models.FileField(upload_to='product_videos/', blank=True, null=True)
    order = models.PositiveIntegerField(default=0)  # For ordering media
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['order', 'created_at']
    
    def __str__(self):
        return f"Media for {self.product.name}"
    
    def save(self, *args, **kwargs):
        # Ensure either image or video is provided, not both
        if self.image and self.video:
            raise ValueError("A media item cannot have both image and video")
        super().save(*args, **kwargs)

# accounts/models.py
class GamingAccessory(models.Model):
    STATUS_CHOICES = [
        ('available', 'Available'),
        ('sale', 'On Sale'),
        ('sold', 'Sold'),
    ]
    
    name = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    sale_price = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True)
    image1 = models.ImageField(upload_to='gaming_accessories/')
    image2 = models.ImageField(upload_to='gaming_accessories/', blank=True, null=True)
    image3 = models.ImageField(upload_to='gaming_accessories/', blank=True, null=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='available')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def is_on_sale(self):
        return self.status == 'sale'
    
    def current_price(self):
        return self.sale_price if self.is_on_sale() else self.price
    
    def has_multiple_images(self):
        return bool(self.image2 or self.image3)
    
    def get_images(self):
        images = [self.image1]
        if self.image2:
            images.append(self.image2)
        if self.image3:
            images.append(self.image3)
        return images
    
    def __str__(self):
        return self.name  



# models.py
from django.db import models
from django.utils import timezone
from django.core.validators import MinValueValidator, MaxValueValidator

class Tournament(models.Model):
    name = models.CharField(max_length=200)
    start_date = models.DateTimeField()
    total_prize_pool = models.DecimalField(max_digits=10, decimal_places=2)
    individual_entry_fee = models.DecimalField(max_digits=6, decimal_places=2)
    team_entry_fee = models.DecimalField(max_digits=6, decimal_places=2)
    rules = models.TextField()
    structure = models.TextField()
    time_limit = models.PositiveIntegerField(help_text="Time limit in minutes")
    allowed_weapons = models.TextField(help_text="Comma-separated list of allowed weapons")
    restricted_weapons = models.TextField(help_text="Comma-separated list of restricted weapons")
    allowed_maps = models.TextField(help_text="Comma-separated list of allowed maps")
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.name

class PrizeDistribution(models.Model):
    tournament = models.ForeignKey(Tournament, on_delete=models.CASCADE, related_name='prizes')
    position = models.PositiveIntegerField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)
    
    class Meta:
        ordering = ['position']
    
    def __str__(self):
        return f"{self.tournament.name} - Position {self.position}"  


# models.py
from django.db import models

class NewsletterSubscription(models.Model):
    email = models.EmailField(unique=True)
    subscribed_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        verbose_name = "Newsletter Subscription"
        verbose_name_plural = "Newsletter Subscriptions"
        ordering = ['-subscribed_at']
    
    def __str__(self):
        return self.email                  
