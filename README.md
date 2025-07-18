# LocalSports - Sports Matchmaking Platform 🏆

A comprehensive Django-based web application that connects sports enthusiasts by facilitating match creation, team management, tournament organization, and real-time communication in local communities.

![Django](https://img.shields.io/badge/Django-5.1.4-green)
![Python](https://img.shields.io/badge/Python-3.8+-blue)
![Bootstrap](https://img.shields.io/badge/Bootstrap-5.3.0-purple)
![Tailwind](https://img.shields.io/badge/TailwindCSS-2.2.19-cyan)

## 🌟 Features

### 🏈 Core Sports Features
- **Match Requests**: Create and join sports matches with skill-based matching
- **Team Management**: Build, manage and recruit for sports teams
- **Tournament Organization**: Create and participate in competitive tournaments
- **Multi-Sport Support**: Football, Basketball, Tennis, Badminton, Cricket
- **Skill Level Matching**: Beginner, Intermediate, and Advanced classifications
- **Location-Based Discovery**: Find matches and teams near you with geolocation

### 👥 Social Features
- **User Profiles**: Customizable profiles with sports preferences and profile pictures
- **Friend System**: Send/receive friend requests and build your sports network
- **Real-time Messaging**: Chat with friends and team members
- **Notifications**: Stay updated on match requests, team activities, and more
- **Activity Feed**: Track sports activities and community engagement

### 🎨 User Experience
- **Responsive Design**: Mobile-first approach optimized for all devices
- **Modern UI**: Glassmorphism effects, gradient backgrounds, and smooth animations
- **Interactive Elements**: AOS scroll animations and dynamic hover effects
- **Accessibility**: User-friendly navigation and intuitive interface

## 🛠️ Technology Stack

### Backend
- **Django 5.1.4**: Robust web framework with ORM
- **SQLite**: Development database (easily configurable for PostgreSQL/MySQL)
- **Django Signals**: Automated notification system
- **Pillow**: Image processing for profile pictures
- **Django Authentication**: Built-in user management

### Frontend
- **HTML5/CSS3**: Semantic markup and modern styling
- **Bootstrap 5.3.0**: Responsive grid system and components
- **Tailwind CSS 2.2.19**: Utility-first CSS framework
- **JavaScript/jQuery**: Interactive functionality and AJAX
- **AOS Library**: Scroll-triggered animations
- **Font Awesome**: Professional icon library
- **Owl Carousel**: Image and content carousels

### Additional Features
- **Geolocation API**: Location-based services
- **Custom CSS**: Advanced styling with gradients and effects
- **Media Management**: Profile picture uploads and static file handling

## 📦 Installation

### Prerequisites
```bash
Python 3.8 or higher
pip (Python package manager)
Git
```

### Quick Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/localsports.git
   cd localsports
   ```

2. **Create and activate virtual environment**
   ```bash
   # Windows
   python -m venv venv
   venv\Scripts\activate
   
   # macOS/Linux
   python3 -m venv venv
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install django==5.1.4
   pip install pillow
   # Add other dependencies as needed
   ```

4. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser (optional)**
   ```bash
   python manage.py createsuperuser
   ```

6. **Collect static files**
   ```bash
   python manage.py collectstatic
   ```

7. **Run development server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Open your browser and navigate to `http://127.0.0.1:8000/`

## 📁 Project Structure

```
sports/
├── 📁 accounts/              # User authentication & profiles
│   ├── models.py            # UserProfile model with geolocation
│   ├── views.py             # Authentication views & profile management
│   ├── forms.py             # User registration & profile forms
│   ├── urls.py              # Authentication URL patterns
│   └── signals.py           # Profile creation signals
├── 📁 chat/                 # Real-time messaging system
│   ├── models.py            # FriendRequest & Message models
│   ├── views.py             # Chat functionality & friend management
│   └── urls.py              # Chat URL patterns
├── 📁 Localsports/          # Core application logic
│   ├── models.py            # Match, Sport, MatchRequest, Notification
│   ├── views.py             # Main application views & business logic
│   ├── forms.py             # Match request & sports forms
│   ├── signals.py           # Notification automation
│   └── urls.py              # Primary URL patterns
├── 📁 Team/                 # Team & tournament management
│   ├── models.py            # Team & Tournament models
│   ├── views.py             # Team creation & management views
│   ├── forms.py             # Team & tournament forms
│   └── urls.py              # Team-related URL patterns
├── 📁 templates/            # HTML templates
│   ├── index.html           # Homepage with feature showcase
│   ├── navbar.html          # Navigation template
│   ├── profile.html         # User profile template
│   ├── 📁 matches/          # Match-related templates
│   ├── 📁 teams/            # Team management templates
│   ├── 📁 chat/             # Chat interface templates
│   └── 📁 tournaments/      # Tournament templates
├── 📁 static/               # Static assets
│   ├── 📁 css/              # Custom CSS files
│   ├── 📁 js/               # JavaScript files
│   ├── 📁 images/           # Image assets & icons
│   └── 📁 bootstrap/        # Bootstrap framework files
├── 📁 media/                # User-uploaded files
│   └── profile_pics/        # Profile picture storage
├── 📁 sports/               # Django project settings
│   ├── settings.py          # Configuration & app registration
│   ├── urls.py              # Main URL configuration
│   └── wsgi.py              # WSGI deployment configuration
├── manage.py                # Django management script
├── db.sqlite3              # SQLite development database
└── README.md               # Project documentation
```

## 🏗️ Key Models & Architecture

### User Management
- **UserProfile**: Extended user information with sports preferences, skill levels, geolocation
- **Custom Authentication**: Django's built-in auth with profile extensions

### Sports System
- **Match**: Basic match entity with location and datetime
- **MatchRequest**: Advanced match requests with skill matching and player capacity
- **Sport**: Sport type definitions and classifications

### Team & Tournament
- **Team**: Team creation with captain/player roles and geolocation
- **Tournament**: Competitive event organization with team registration

### Social Features
- **FriendRequest**: Friend system with pending/accepted/rejected states
- **Message**: Real-time messaging between users
- **Notification**: Automated notifications for platform activities

## 🚀 Usage Guide

### For Players
1. **Register & Setup Profile**
   - Create account with email/username
   - Complete profile with sports preferences and skill level
   - Upload profile picture and set location

2. **Discover Matches**
   - Browse available match requests in your area
   - Filter by sport type, skill level, and location
   - Join matches that suit your schedule and skill level

3. **Connect with Community**
   - Send friend requests to other players
   - Chat with friends and teammates
   - Receive notifications for match updates

### For Team Captains
1. **Create & Manage Teams**
   - Set up sports teams with detailed information
   - Recruit players through the platform
   - Organize team activities and matches

2. **Team Communication**
   - Chat with team members
   - Coordinate practices and games
   - Manage team roster and activities

### For Tournament Organizers
1. **Tournament Setup**
   - Create competitive tournaments
   - Set registration periods and requirements
   - Manage participating teams

2. **Event Management**
   - Track tournament progress
   - Coordinate match schedules
   - Monitor team participation

## 🎯 Key Features in Detail

### 🏃‍♂️ Smart Match System
- **Skill-based Matching**: Automatic matching based on skill levels
- **Location Proximity**: Find matches near your location using geolocation
- **Capacity Management**: Track available spots and player limits
- **Real-time Updates**: Live updates on match availability

### 👥 Advanced Team Management
- **Captain Controls**: Special permissions for team leaders
- **Member Recruitment**: Invite system for team building
- **Team Statistics**: Track team performance and activities
- **Multi-sport Support**: Create teams for different sports

### 🏆 Tournament System
- **Flexible Tournament Creation**: Support for various tournament formats
- **Team Registration**: Easy signup process for teams
- **Progress Tracking**: Monitor tournament advancement
- **Sport-specific Rules**: Different rules for different sports

### 💬 Communication Hub
- **Real-time Messaging**: Instant chat between users
- **Friend Network**: Build connections within the sports community
- **Notification System**: Stay informed about all activities
- **Group Communication**: Team and tournament group chats

## ⚙️ Configuration

### Environment Setup
```python
# settings.py key configurations
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'Localsports',      # Core sports functionality
    'accounts',         # User management
    'Team',            # Team & tournament management
    'chat',            # Messaging system
]
```

### Database Configuration
```python
# For production, replace with PostgreSQL/MySQL
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

### Media Files Setup
```python
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'
```

## 🚀 Deployment

### Production Considerations
1. **Database**: Migrate from SQLite to PostgreSQL or MySQL
2. **Static Files**: Configure proper static file serving (nginx/Apache)
3. **Security**: Update SECRET_KEY and set DEBUG=False
4. **Media Storage**: Set up cloud storage for user uploads
5. **Environment Variables**: Use environment variables for sensitive data

### Deployment Checklist
- [ ] Update ALLOWED_HOSTS
- [ ] Configure production database
- [ ] Set up static file serving
- [ ] Configure email backend for notifications
- [ ] Set up SSL certificates
- [ ] Configure backup strategies

## 🧪 Testing

### Running Tests
```bash
# Run all tests
python manage.py test

# Run tests for specific app
python manage.py test Localsports
python manage.py test accounts
python manage.py test Team
python manage.py test chat
```

## 🤝 Contributing

1. **Fork the repository**
2. **Create feature branch**
   ```bash
   git checkout -b feature/AmazingFeature
   ```
3. **Commit changes**
   ```bash
   git commit -m 'Add some AmazingFeature'
   ```
4. **Push to branch**
   ```bash
   git push origin feature/AmazingFeature
   ```
5. **Open Pull Request**

### Development Guidelines
- Follow Django best practices
- Write descriptive commit messages
- Add tests for new features
- Update documentation as needed
- Ensure mobile responsiveness

## 📋 Future Enhancements

- [ ] **Mobile App**: React Native or Flutter mobile application
- [ ] **Payment Integration**: Premium features and tournament fees
- [ ] **Advanced Analytics**: Player statistics and performance tracking
- [ ] **Video Calls**: Integrated video chat for remote team meetings
- [ ] **Live Scoring**: Real-time match score updates
- [ ] **Weather Integration**: Weather-based match recommendations
- [ ] **AI Matching**: Machine learning for better player matching
- [ ] **Social Media Integration**: Share achievements on social platforms

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Django Community**: For the excellent web framework
- **Bootstrap Team**: For responsive UI components
- **Tailwind CSS**: For utility-first CSS framework
- **Font Awesome**: For comprehensive icon library
- **AOS Library**: For smooth scroll animations
- **Open Source Community**: For continuous inspiration and support

## 📞 Support & Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/localsports/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/localsports/discussions)
- **Email**: support@localsports.com
- **Documentation**: [Wiki](https://github.com/yourusername/localsports/wiki)

## 📊 Project Statistics

- **Models**: 8 core models
- **Apps**: 4 Django applications
- **Templates**: 15+ responsive templates
- **Features**: 20+ key features
- **Sports Supported**: 5 different sports
- **Tech Stack**: 10+ technologies

---

**LocalSports** - Connecting communities through sports! 🏀⚽🏈🎾🏏

*Build stronger communities, one match at a time.* ✨