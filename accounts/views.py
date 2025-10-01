from django.shortcuts import render
from .models import Account

def home(request):
    accounts = Account.objects.filter(available=True)
    return render(request, 'accounts/home.html', {'accounts': accounts})

  # accounts/views.py
from django.shortcuts import render, redirect
from django.contrib import messages
from .models import Review  # Import the Review model

# accounts/views.py
from .models import GamingAccessory


# accounts/views.py
def home(request):
    # Keep the approved filter since you added the field
    reviews = Review.objects.all().order_by('-created_at')[:10]
    products = Product.objects.filter(status__in=['available', 'sale']).order_by('-created_at')[:8]
    accessories = GamingAccessory.objects.filter(status__in=['available', 'sale']).order_by('-created_at')[:4]
    sold_products = Product.objects.filter(status='sold').order_by('-updated_at')[:4]
    
    context = {
        'reviews': reviews,
        'products': products,
        'accessories': accessories,
        'sold_products': sold_products,
    }
    return render(request, 'home.html', context)

def submit_review(request):
    if request.method == 'POST':
        full_name = request.POST.get('full_name')
        comment = request.POST.get('comment')
        rating = request.POST.get('rating')
        photo = request.FILES.get('photo')
        user_type = request.POST.get('user_type', '')
        
        # Validate required fields
        if not all([full_name, comment, rating]):
            messages.error(request, 'Please fill in all required fields.')
            return redirect('home')
        
        # Save to database
        try:
            review = Review(
                full_name=full_name,
                comment=comment,
                rating=int(rating),
                photo=photo,
                user_type=user_type if user_type else None
            )
            review.save()
            
            messages.success(request, 'Thank you for your review!')
        except Exception as e:
            messages.error(request, f'Error saving review: {str(e)}')
        
        return redirect('home')
    
    # If it's a GET request, redirect to home
    return redirect('home')

    # accounts/views.py
from django.shortcuts import render
from .models import Product

def shop(request):
    # Get all available products (not sold)
    products = Product.objects.exclude(status='sold').order_by('-created_at')
    
    context = {
        'products': products
    }
    return render(request, 'shop.html', context)


# views.py
from django.shortcuts import render, get_object_or_404
from django.utils import timezone
from .models import Tournament

def battle_view(request):
    # Get the active tournament or the next upcoming one
    try:
        tournament = Tournament.objects.filter(is_active=True).latest('start_date')
    except Tournament.DoesNotExist:
        # If no active tournament, get the next upcoming one
        tournament = Tournament.objects.filter(
            start_date__gte=timezone.now()
        ).order_by('start_date').first()
    
    if not tournament:
        # No tournaments available
        return render(request, 'battle.html', {'tournament': None})
    
    # Get prize distribution
    prizes = tournament.prizes.all()
    
    context = {
        'tournament': tournament,
        'prizes': prizes,
    }
    
    return render(request, 'battle.html', context)    


from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
import os
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json

def request_page(request):
    """View for the account request and selling page"""
    
    # Handle AJAX requests for form submissions
    if request.method == 'POST' and request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return handle_ajax_form(request)
    
    # Handle traditional form submissions (non-AJAX)
    elif request.method == 'POST':
        return handle_traditional_form(request)
    
    # GET request - just render the template
    return render(request, 'request.html')

def handle_ajax_form(request):
    """Handle AJAX form submissions"""
    try:
        # Check which form was submitted
        if 'seller_name' in request.POST:  # Sell form (AJAX)
            seller_name = request.POST.get('seller_name', '').strip()
            seller_contact = request.POST.get('seller_contact', '').strip()
            account_title = request.POST.get('account_title', '').strip()
            price = request.POST.get('price', '').strip()
            account_level = request.POST.get('account_level', '').strip()
            account_details = request.POST.get('account_details', '').strip()
            
            # Validate required fields
            if not all([seller_name, seller_contact, account_title, price, account_details]):
                return JsonResponse({
                    'success': False,
                    'message': 'Please fill in all required fields.'
                })
            
            # Handle file uploads
            uploaded_files = request.FILES.getlist('media_files')
            file_paths = []
            
            for file in uploaded_files:
                # Save files to media directory
                path = default_storage.save(f'account_sales/{file.name}', ContentFile(file.read()))
                file_paths.append(path)
                print(f"Saved file: {path}")
            
            # Send email notification
            try:
                # HTML email content
                html_message = f"""
                <html>
                <body>
                    <h2>New Account Sale Request</h2>
                    <p><strong>Seller Name:</strong> {seller_name}</p>
                    <p><strong>Contact Info:</strong> {seller_contact}</p>
                    <p><strong>Account Title:</strong> {account_title}</p>
                    <p><strong>Asking Price:</strong> ${price}</p>
                    <p><strong>Account Level:</strong> {account_level}</p>
                    <p><strong>Account Details:</strong></p>
                    <p>{account_details.replace(chr(10), '<br>')}</p>
                    <p><strong>Files Uploaded:</strong> {len(file_paths)}</p>
                    <hr>
                    <p><em>Sent from Cauxie Sales website</em></p>
                </body>
                </html>
                """
                
                # Send email with HTML content
                send_mail(
                    subject=f'New Account for Sale: {account_title}',
                    message=f"""
                    New account listing:
                    
                    Seller: {seller_name}
                    Contact: {seller_contact}
                    Title: {account_title}
                    Price: ${price}
                    Level: {account_level}
                    Details: {account_details}
                    Files uploaded: {len(file_paths)}
                    """,  # Plain text fallback
                    html_message=html_message,  # HTML version
                    from_email=settings.DEFAULT_FROM_EMAIL,
                    recipient_list=[settings.ADMIN_EMAIL],
                    fail_silently=False,
                )
                
                return JsonResponse({
                    'success': True,
                    'message': 'Your account has been listed successfully! We will contact you soon.'
                })
                
            except Exception as e:
                print(f"Email error: {e}")
                return JsonResponse({
                    'success': False,
                    'message': 'Error sending email. Please try again or contact us directly.'
                })
        
        elif 'name' in request.POST:  # Request form (AJAX)
            # Handle the request form similarly if needed
            name = request.POST.get('name', '').strip()
            phone = request.POST.get('phone', '').strip()
            account_type = request.POST.get('accountType', '').strip()
            budget = request.POST.get('budget', '').strip()
            details = request.POST.get('details', '').strip()
            
            # Your existing request form logic here...
            # Return JsonResponse for AJAX
            
            return JsonResponse({
                'success': True,
                'message': 'Request submitted successfully!'
            })
    
    except Exception as e:
        print(f"AJAX form error: {e}")
        return JsonResponse({
            'success': False,
            'message': 'An unexpected error occurred. Please try again.'
        })
    
    return JsonResponse({'success': False, 'message': 'Invalid form submission'})

def handle_traditional_form(request):
    """Handle traditional form submissions (non-AJAX)"""
    if 'name' in request.POST:  # Request form
        name = request.POST.get('name')
        phone = request.POST.get('phone')
        account_type = request.POST.get('accountType')
        budget = request.POST.get('budget')
        details = request.POST.get('details')
        
        # Process the request
        print(f"Account Request: {name}, {phone}, {account_type}, ${budget}")
        print(f"Details: {details}")
        
        try:
            send_mail(
                f'New Account Request from {name}',
                f"""
                New account request received:
                
                Name: {name}
                Phone: {phone}
                Account Type: {account_type}
                Budget: ${budget}
                Details: {details}
                """,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email error: {e}")
        
        messages.success(request, 'Your request has been submitted successfully!')
        return redirect('request')
        
    elif 'sellerName' in request.POST:  # Sell form
        seller_name = request.POST.get('sellerName')
        seller_contact = request.POST.get('sellerContact')
        account_title = request.POST.get('accountTitle')
        price = request.POST.get('price')
        account_level = request.POST.get('accountLevel')
        account_details = request.POST.get('accountDetails')
        
        # Process the selling form
        print(f"Account for Sale: {seller_name}, {seller_contact}, {account_title}")
        print(f"Price: ${price}, Level: {account_level}")
        print(f"Details: {account_details}")
        
        # Handle file uploads
        uploaded_files = request.FILES.getlist('mediaUpload')
        file_paths = []
        
        for file in uploaded_files:
            path = default_storage.save(f'account_sales/{file.name}', ContentFile(file.read()))
            file_paths.append(path)
            print(f"Saved file: {path}")
        
        try:
            send_mail(
                f'New Account for Sale: {account_title}',
                f"""
                New account listing:
                
                Seller: {seller_name}
                Contact: {seller_contact}
                Title: {account_title}
                Price: ${price}
                Level: {account_level}
                Details: {account_details}
                Files uploaded: {len(file_paths)}
                """,
                settings.DEFAULT_FROM_EMAIL,
                [settings.ADMIN_EMAIL],
                fail_silently=False,
            )
        except Exception as e:
            print(f"Email error: {e}")
        
        messages.success(request, 'Your account has been sent to the team!')
        return redirect('request')  


def privacy(request):
    """View for displaying the privacy policy page"""
    context = {
        'title': 'Privacy Policy - Cauxie Sales',
    }
    return render(request, 'privacy.html', context)

def terms(request):
    """View for displaying the terms of service page"""
    context = {
        'title': 'Terms of Service - Cauxie Sales',
    }
    return render(request, 'terms.html', context)

def about(request):
    """View for displaying the about page"""
    context = {
        'title': 'About Us - Cauxie Sales',
    }
    return render(request, 'about.html', context)

# views.py
from django.shortcuts import redirect
from django.contrib import messages
from django.http import JsonResponse
from .forms import NewsletterSubscriptionForm

def subscribe_newsletter(request):
    if request.method == "POST":
        form = NewsletterSubscriptionForm(request.POST)
        if form.is_valid():
            subscription = form.save()
            messages.success(request, "Successfully subscribed to our newsletter!")
            
            # Return JSON response for AJAX
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': True,
                    'message': 'Successfully subscribed to our newsletter!'
                })
        else:
            messages.error(request, "There was an error with your subscription.")
            
            if request.headers.get('x-requested-with') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'There was an error with your subscription.',
                    'errors': form.errors
                })
    
    return redirect('home')  # Redirect back to home page  


from django.http import HttpResponse
from django.core.management import call_command
from io import StringIO
import os

def create_superuser_view(request):
    # Add a secret key for security
    if request.GET.get('key') != 'your-secret-key-123':
        return HttpResponse('Unauthorized', status=403)
    
    # Check if superuser already exists
    from django.contrib.auth.models import User
    if User.objects.filter(is_superuser=True).exists():
        return HttpResponse('Superuser already exists')
    
    # Create superuser
    try:
        User.objects.create_superuser(
            username='admin',
            email='admin@example.com',
            password='temp_password_123'
        )
        return HttpResponse('Superuser created successfully! Username: admin, Password: temp_password_123')
    except Exception as e:
        return HttpResponse(f'Error: {str(e)}')          