# accounts/admin.py
from django.contrib import admin
from django import forms
from .models import Product, Review, ProductMedia, GamingAccessory, Tournament, PrizeDistribution, NewsletterSubscription

class ProductMediaForm(forms.ModelForm):
    class Meta:
        model = ProductMedia
        fields = ['image', 'video', 'order']
    
    def clean(self):
        cleaned_data = super().clean()
        image = cleaned_data.get('image')
        video = cleaned_data.get('video')
        
        # Check if both image and video are provided
        if image and video:
            raise forms.ValidationError("A media item cannot have both image and video. Please choose either an image OR a video.")
        
        return cleaned_data

class ProductMediaInline(admin.TabularInline):
    model = ProductMedia
    form = ProductMediaForm
    extra = 1
    fields = ['image', 'video', 'order']
    verbose_name = "Media File"
    verbose_name_plural = "Media Files"

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'sale_price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    search_fields = ['name', 'description']
    inlines = [ProductMediaInline]
    fieldsets = [
        (None, {
            'fields': ['name', 'description', 'status']
        }),
        ('Pricing', {
            'fields': ['price', 'sale_price']
        }),
    ]

@admin.register(ProductMedia)
class ProductMediaAdmin(admin.ModelAdmin):
    list_display = ['product', 'media_type', 'order', 'created_at']
    list_filter = ['product', 'created_at']
    search_fields = ['product__name']
    form = ProductMediaForm
    
    def media_type(self, obj):
        return obj.media_type
    media_type.short_description = 'Media Type'

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['full_name', 'comment']

@admin.register(GamingAccessory)
class GamingAccessoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status', 'price']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'description', 'status')
        }),
        ('Pricing', {
            'fields': ('price', 'sale_price')
        }),
        ('Images', {
            'fields': ('image1', 'image2', 'image3')
        }),
    )

class PrizeDistributionInline(admin.TabularInline):
    model = PrizeDistribution
    extra = 1

@admin.register(Tournament)
class TournamentAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_date', 'total_prize_pool', 'is_active']
    list_filter = ['is_active', 'start_date']
    inlines = [PrizeDistributionInline]
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'start_date', 'is_active')
        }),
        ('Financials', {
            'fields': ('total_prize_pool', 'individual_entry_fee', 'team_entry_fee')
        }),
        ('Rules & Settings', {
            'fields': ('rules', 'structure', 'time_limit', 'allowed_weapons', 'restricted_weapons', 'allowed_maps')
        }),
    )

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']
    list_editable = ['is_active']
