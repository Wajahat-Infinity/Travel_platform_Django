from django.core.management.base import BaseCommand
from django.core.files.base import ContentFile
from django.utils import timezone
from datetime import date, timedelta
import os

from src.web.website.models import (
    HeroSlider, PopularTour, TopActivity, BlogPost, 
    ClientLogo, NewsletterSubscriber, Testimonial, SiteSettings
)
from src.web.agency.models import Agency, TourPackage

class Command(BaseCommand):
    help = 'Populate homepage with sample data'

    def handle(self, *args, **options):
        self.stdout.write('Creating sample data for homepage...')
        
        # Create site settings
        site_settings, created = SiteSettings.objects.get_or_create(
            pk=1,
            defaults={
                'site_name': 'Travel Platform',
                'hero_title': 'Are You Ready...',
                'hero_subtitle': 'To explore new things?',
                'explore_title': 'Explore more with us',
                'explore_description': 'Join 2000+ locals & 1200+ contributors from 3000 cities',
                'discount_title': 'Enjoy Your Holiday with 50% Discount',
                'discount_description': 'Nemo enim ipsam voluptatem quia voluptas sit aspernatur',
                'newsletter_title': 'Subscribe to Get Special Offers',
                'newsletter_description': 'Newsletter Sign up',
                'featured_in_title': 'We were featured in',
            }
        )
        
        if created:
            self.stdout.write(self.style.SUCCESS('✓ Site settings created'))
        else:
            self.stdout.write(self.style.SUCCESS('✓ Site settings already exist'))
        
        # Create sample testimonials (keeping as requested)
        testimonials_data = [
            {
                'name': 'Leroy Bell',
                'country': 'United States',
                'content': 'Excepteur sint occaecat cupidatat non proident sunt in culpa officia deserunt mollit anim laborum sint occaecat cupidatat non proident. Occaecat cupidatat non proident des.',
                'rating': 5,
                'order': 1
            },
            {
                'name': 'Richard Pam',
                'country': 'Canada',
                'content': 'Excepteur sint occaecat cupidatat non proident sunt in culpa officia deserunt mollit anim laborum sint occaecat cupidatat non proident. Occaecat cupidatat non proident des.',
                'rating': 5,
                'order': 2
            },
            {
                'name': 'Luke Jacobs',
                'country': 'Australia',
                'content': 'Excepteur sint occaecat cupidatat non proident sunt in culpa officia deserunt mollit anim laborum sint occaecat cupidatat non proident. Occaecat cupidatat non proident des.',
                'rating': 5,
                'order': 3
            },
            {
                'name': 'Chulbul Panday',
                'country': 'Italy',
                'content': 'Excepteur sint occaecat cupidatat non proident sunt in culpa officia deserunt mollit anim laborum sint occaecat cupidatat non proident. Occaecat cupidatat non proident des.',
                'rating': 5,
                'order': 4
            }
        ]
        
        for testimonial_data in testimonials_data:
            testimonial, created = Testimonial.objects.get_or_create(
                name=testimonial_data['name'],
                defaults=testimonial_data
            )
            if created:
                self.stdout.write(f'✓ Testimonial "{testimonial.name}" created')
        
        # Create sample top activities
        activities_data = [
            {'name': 'Cultural Trecks', 'order': 1},
            {'name': 'Carnival', 'order': 2},
            {'name': 'Murano', 'order': 3},
            {'name': 'Eat + Drink', 'order': 4},
            {'name': 'Gondola Ride', 'order': 5},
            {'name': 'Museum Tickets', 'order': 6},
            {'name': 'Sightseeing', 'order': 7},
            {'name': 'Outdoor Activities', 'order': 8},
        ]
        
        for activity_data in activities_data:
            activity, created = TopActivity.objects.get_or_create(
                name=activity_data['name'],
                defaults={
                    **activity_data,
                    'description': f'Experience amazing {activity_data["name"].lower()} activities',
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'✓ Activity "{activity.name}" created')
        
        # Create sample blog posts
        blog_posts_data = [
            {
                'title': 'Best Scandinavian Accommodation – Treat Yourself',
                'slug': 'best-scandinavian-accommodation',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'excerpt': 'Discover the best places to stay in Scandinavia',
                'author_name': 'Leroy Bell',
                'categories': 'Travel,lifestyle',
                'post_format': 'TEXT',
                'read_time': 5,
                'is_published': True
            },
            {
                'title': 'Amazing Places to Stay in Norway',
                'slug': 'amazing-places-norway',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'excerpt': 'Explore the most beautiful accommodations in Norway',
                'author_name': 'Phillip Hunt',
                'categories': 'Video',
                'post_format': 'VIDEO',
                'read_time': 4,
                'is_published': True
            },
            {
                'title': 'Feel Like Home on Your Business Trip',
                'slug': 'business-trip-accommodation',
                'content': 'Lorem ipsum dolor sit amet, consectetur adipiscing elit. Sed do eiusmod tempor incididunt ut labore et dolore magna aliqua.',
                'excerpt': 'Make your business trips more comfortable',
                'author_name': 'Luke Jacobs',
                'categories': 'audio',
                'post_format': 'AUDIO',
                'read_time': 3,
                'is_published': True
            }
        ]
        
        for post_data in blog_posts_data:
            post, created = BlogPost.objects.get_or_create(
                slug=post_data['slug'],
                defaults=post_data
            )
            if created:
                self.stdout.write(f'✓ Blog post "{post.title}" created')
        
        # Create sample client logos
        client_logos_data = [
            {'name': 'Client 1', 'order': 1},
            {'name': 'Client 2', 'order': 2},
            {'name': 'Client 3', 'order': 3},
            {'name': 'Client 4', 'order': 4},
            {'name': 'Client 5', 'order': 5},
            {'name': 'Client 6', 'order': 6},
        ]
        
        for logo_data in client_logos_data:
            logo, created = ClientLogo.objects.get_or_create(
                name=logo_data['name'],
                defaults={
                    **logo_data,
                    'is_active': True
                }
            )
            if created:
                self.stdout.write(f'✓ Client logo "{logo.name}" created')
        
        # Create sample newsletter subscribers
        subscribers_data = [
            'john@example.com',
            'jane@example.com',
            'bob@example.com',
        ]
        
        for email in subscribers_data:
            subscriber, created = NewsletterSubscriber.objects.get_or_create(
                email=email,
                defaults={'is_active': True}
            )
            if created:
                self.stdout.write(f'✓ Newsletter subscriber "{email}" created')
        
        self.stdout.write(self.style.SUCCESS('\n✓ Sample data creation completed!'))
        self.stdout.write('\nNote: You can now add content through the Django admin interface:')
        self.stdout.write('- Hero sliders: Add images and content for the hero section')
        self.stdout.write('- Popular tours: Link existing tour packages from agencies')
        self.stdout.write('- Activities: Add images for the flip-box activities')
        self.stdout.write('- Blog posts: Add featured images and full content')
        self.stdout.write('- Client logos: Add actual logo images')
        self.stdout.write('- Testimonials: Add profile images for testimonials') 