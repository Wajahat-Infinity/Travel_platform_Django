# 🚀 Travel Platform - Django Web Application

A comprehensive travel booking platform built with Django that connects travelers with travel agencies and local guides. This platform provides a complete ecosystem for tour package management, booking systems, and travel services.

## 🌟 Features

### 👥 Multi-User System
- **Travelers**: Browse packages, book tours, and manage travel preferences
- **Travel Agencies**: Create and manage tour packages, hotels, vehicles, and places
- **Local Guides**: Offer guided tours with language skills and certifications
- **Admin Panel**: Complete administrative control and monitoring

### 🏨 Agency Management
- **Tour Packages**: Create Standard, Premium, and Luxury packages
- **Hotel Management**: Add hotels with ratings, pricing, and images
- **Vehicle Fleet**: Manage vehicles with capacity and scheduling
- **Destination Management**: Add tourist places with descriptions and images
- **Branch Management**: Multiple agency branches with contact information

### 🎯 Local Guide Services
- **Professional Profiles**: Experience, skills, and availability management
- **Language Proficiency**: Multi-language support with proficiency levels
- **Certification System**: Professional certifications and credentials
- **Booking Management**: Direct booking system for guide services

### 📅 Booking System
- **Tour Bookings**: Complete booking system with payment integration
- **Trip Bookings**: Individual trip bookings with agency management
- **Guide Bookings**: Direct bookings with local guides
- **Payment Processing**: Stripe integration for secure payments
- **Booking Status**: Pending, confirmed, completed, cancelled, refunded

### 🌐 Website Features
- **Responsive Design**: Modern, mobile-friendly interface
- **Blog System**: Travel articles and content management
- **Testimonials**: Customer reviews and ratings
- **Newsletter**: Email subscription system
- **Hero Sliders**: Dynamic homepage content
- **Popular Tours**: Featured tour packages
- **Client Logos**: Partner and client showcase

### 📊 Content Management
- **Blog Posts**: Rich text editor with categories and formats
- **Testimonials**: Customer feedback with ratings
- **Site Settings**: Configurable website content and SEO
- **Media Management**: Image uploads for profiles, hotels, vehicles, places

## 🛠️ Technology Stack

### Backend
- **Django 5.2.3**: Web framework
- **Python 3.12.1**: Programming language
- **SQLite/PostgreSQL**: Database
- **Django Crispy Forms**: Form styling
- **Django Allauth**: Authentication system
- **Django REST Framework**: API development
- **Stripe**: Payment processing

### Frontend
- **Bootstrap**: CSS framework
- **jQuery**: JavaScript library
- **Font Awesome**: Icons
- **Responsive Design**: Mobile-first approach

### Additional Libraries
- **Django Resized**: Image processing
- **Scikit-learn**: Machine learning (destination prediction)
- **Pandas**: Data manipulation
- **NumPy**: Numerical computing

## 📁 Project Structure

```
Travel_platform_Django/
├── core/                          # Django settings and configuration
├── src/                           # Main application source
│   ├── accounts/                  # User authentication and profiles
│   ├── administration/            # Admin panel and management
│   └── web/                       # Web applications
│       ├── agency/                # Travel agency management
│       ├── booking/               # Booking system
│       ├── local_guide/           # Local guide services
│       ├── traveler/              # Traveler profiles and preferences
│       └── website/               # Website content and frontend
├── destination_predictor/         # ML-based destination prediction
├── static/                        # Static files (CSS, JS, images)
├── media/                         # User-uploaded files
├── templates/                     # Global templates
├── test_cases/                    # Test files
└── venv/                          # Virtual environment
```

## 🚀 Installation & Setup

### Prerequisites
- Python 3.12+
- pip (Python package installer)
- Git

### Step 1: Clone the Repository
```bash
git clone <repository-url>
cd Travel_platform_Django
```

### Step 2: Create Virtual Environment
```bash
python -m venv venv
# On Windows
venv\Scripts\activate
# On macOS/Linux
source venv/bin/activate
```

### Step 3: Install Dependencies
```bash
pip install -r requirements.txt
```

### Step 4: Environment Configuration
1. Copy `example.env` to `.env`
2. Update the environment variables:
   ```env
   DEBUG=True
   SECRET_KEY=your-secret-key
   DATABASE_URL=your-database-url
   EMAIL_HOST=smtp.gmail.com
   EMAIL_HOST_USER=your-email@gmail.com
   EMAIL_HOST_PASSWORD=your-email-password
   STRIPE_PUBLIC_KEY=your-stripe-public-key
   STRIPE_SECRET_KEY=your-stripe-secret-key
   ```

### Step 5: Database Setup
```bash
python manage.py makemigrations
python manage.py migrate
```

### Step 6: Create Superuser
```bash
python manage.py createsuperuser
```

### Step 7: Run Development Server
```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000/` to access the application.

## 📊 Database Schema

The application includes **25+ database tables** with comprehensive relationships:

### Core Tables
- **User**: Custom user model with role-based access
- **Traveler**: Customer profiles with travel preferences
- **Agency**: Travel agencies with complete business information
- **LocalGuide**: Professional guides with skills and certifications

### Business Tables
- **TourPackage**: Tour packages with pricing and components
- **Hotel**: Hotel management with ratings and images
- **Vehicle**: Vehicle fleet with capacity and scheduling
- **Place**: Tourist destinations with descriptions
- **Booking**: Complete booking system with payment tracking

### Content Tables
- **BlogPost**: Travel articles and content
- **Testimonial**: Customer reviews and ratings
- **SiteSettings**: Configurable website content
- **NewsletterSubscriber**: Email subscription management

## 🔧 Configuration

### Django Settings
- **DEBUG**: Set to `False` in production
- **ALLOWED_HOSTS**: Configure for your domain
- **STATIC_ROOT**: Set for production static file serving
- **MEDIA_ROOT**: Configure for file uploads

### Email Configuration
- **EMAIL_BACKEND**: SMTP configuration for notifications
- **DEFAULT_FROM_EMAIL**: Set your support email

### Payment Configuration
- **Stripe Keys**: Configure for payment processing
- **Webhook Endpoints**: Set up for payment confirmations

## 🧪 Testing

Run the test suite:
```bash
python manage.py test
```

## 📱 API Endpoints

The application includes REST API endpoints for:
- User authentication and registration
- Tour package management
- Booking operations
- Guide services
- Content management

## 🔒 Security Features

- **CSRF Protection**: Built-in Django CSRF protection
- **XSS Prevention**: Template auto-escaping
- **SQL Injection Protection**: Django ORM protection
- **Authentication**: Secure user authentication system
- **File Upload Security**: Validated file uploads
- **Payment Security**: Stripe secure payment processing

## 🚀 Deployment

### Production Checklist
- [ ] Set `DEBUG=False`
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure email settings
- [ ] Set up SSL/HTTPS
- [ ] Configure payment webhooks
- [ ] Set up monitoring and logging

### Recommended Hosting
- **Heroku**: Easy deployment with PostgreSQL
- **DigitalOcean**: VPS with full control
- **AWS**: Scalable cloud infrastructure
- **Vercel**: Frontend deployment option

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👥 Team

- **Developer**: [Your Name]
- **Design**: [Designer Name]
- **Testing**: [Tester Name]

## 📞 Support

For support and questions:
- **Email**: support@travelplatform.com
- **Documentation**: [Link to documentation]
- **Issues**: [GitHub Issues](https://github.com/your-repo/issues)

## 🔄 Version History

- **v1.0.0** - Initial release with core features
- **v1.1.0** - Added payment integration
- **v1.2.0** - Enhanced booking system
- **v1.3.0** - Added local guide features

---

**Made with ❤️ using Django**
