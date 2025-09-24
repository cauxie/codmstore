# accounts/admin.py
from django.contrib import admin
from .models import Product, Review

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'price', 'status', 'created_at']
    list_filter = ['status', 'created_at']
    list_editable = ['status', 'price']
    search_fields = ['name', 'description']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Review)
class ReviewAdmin(admin.ModelAdmin):
    list_display = ['full_name', 'rating', 'created_at']
    list_filter = ['rating', 'created_at']
    search_fields = ['full_name', 'comment']

# accounts/admin.py
from django.contrib import admin
from .models import GamingAccessory

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

# admin.py
from django.contrib import admin
from .models import Tournament, PrizeDistribution

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

# admin.py
from django.contrib import admin
from .models import NewsletterSubscription

@admin.register(NewsletterSubscription)
class NewsletterSubscriptionAdmin(admin.ModelAdmin):
    list_display = ['email', 'subscribed_at', 'is_active']
    list_filter = ['is_active', 'subscribed_at']
    search_fields = ['email']
    readonly_fields = ['subscribed_at']
    list_editable = ['is_active']       