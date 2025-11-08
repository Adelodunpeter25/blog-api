# Blog API - Django REST Framework

A modern blog API with authentication, social features, and optimized image handling.

## ✨ Key Features

- **Authentication** - Email/password + Google OAuth with JWT tokens
- **User Profiles** - Bio, avatar, social links, following system
- **Blog Posts** - CRUD operations, categories, tags, featured posts, drafts
- **Social Features** - Post reactions (like/love/bookmark), reading lists, comments
- **Image Optimization** - Auto-resize, WebP conversion, multiple sizes
- **Advanced API** - Search, filtering, pagination, analytics

## 📋 Requirements

- Python 3.8+
- Django 5.2+
- PostgreSQL/SQLite

## 🛠️ Installation

1. **Clone and setup**
```bash
git clone https://github.com/Adelodunpeter25/blog-api.git
cd blog-api
uv sync
```

2. **Configure environment**
```bash
cp .env.example .env
# Edit .env with your settings
```

3. **Setup database**
```bash
uv run python manage.py migrate
uv run python manage.py createsuperuser
```

4. **Run server**
```bash
uv run python manage.py runserver
```

## 📚 API Documentation

### Authentication Endpoints

```http
POST /api/auth/register/     # Register
POST /api/auth/login/        # Login
POST /api/auth/google/       # Google OAuth
POST /api/auth/logout/       # Logout
```

### Main Endpoints

```http
# Posts
GET  /api/posts/             # List posts (?search=term&category=slug)
POST /api/posts/             # Create post
GET  /api/posts/{slug}/      # Get post
GET  /api/posts/featured/    # Featured posts

# Social
POST /api/reactions/react/   # Like/love/bookmark post
GET  /api/reading-list/      # Get saved posts
POST /api/users/{id}/follow/ # Follow user

# Other: /api/users/, /api/categories/, /api/tags/, /api/comments/
```

### Example Usage

```bash
# Register
curl -X POST http://localhost:8000/api/auth/register/ \
  -H "Content-Type: application/json" \
  -d '{"email":"user@example.com","password":"password123"}'

# Create post (with auth token)
curl -X POST http://localhost:8000/api/posts/ \
  -H "Authorization: Bearer YOUR_TOKEN" \
  -d '{"title":"My Post","content":"Content here","status":"published"}'
```

## 🧪 Testing

```bash
uv run python manage.py test
```

## 🚀 Production

- Set `DEBUG=False`
- Use PostgreSQL database
- Configure static file serving
- Set proper CORS origins

## 📄 License

MIT License - see LICENSE file for details.

---

**Built with Django REST Framework**