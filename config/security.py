from flask_talisman import Talisman
from flask_limiter import Limiter
from flask_limiter.util import get_remote_address

def configure_security(app):
    """Configure security features for the Flask application."""
    
    # Enable HTTPS-only
    Talisman(app,
             force_https=True,
             strict_transport_security=True,
             session_cookie_secure=True,
             content_security_policy={
                 'default-src': "'self'",
                 'script-src': ["'self'", "'unsafe-inline'"],
                 'style-src': ["'self'", "'unsafe-inline'"],
                 'img-src': ["'self'", 'data:', 'https:'],
                 'connect-src': ["'self'", 'https:'],
                 'font-src': ["'self'", 'https:', 'data:'],
             })
    
    # Rate limiting
    limiter = Limiter(
        app,
        key_func=get_remote_address,
        default_limits=["200 per day", "50 per hour"]
    )
    
    # Add rate limits to specific endpoints
    @limiter.limit("1 per second")
    @app.route("/process_voice", methods=["POST"])
    def process_voice_limit():
        return app.view_functions['process_voice']()
    
    # Security headers
    @app.after_request
    def add_security_headers(response):
        response.headers['X-Content-Type-Options'] = 'nosniff'
        response.headers['X-Frame-Options'] = 'SAMEORIGIN'
        response.headers['X-XSS-Protection'] = '1; mode=block'
        response.headers['Referrer-Policy'] = 'strict-origin-when-cross-origin'
        response.headers['Permissions-Policy'] = 'geolocation=(), microphone=(self), camera=(self)'
        return response
    
    # CSRF Protection
    @app.before_request
    def csrf_protect():
        if app.config['ENV'] == 'production':
            if request.method == "POST":
                token = session.get('_csrf_token', None)
                if not token or token != request.form.get('_csrf_token'):
                    abort(403)

    def generate_csrf_token():
        if '_csrf_token' not in session:
            session['_csrf_token'] = secrets.token_urlsafe(32)
        return session['_csrf_token']
    
    app.jinja_env.globals['csrf_token'] = generate_csrf_token 