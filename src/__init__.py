from flask import Flask

def create_app():
    app = Flask(__name__)
    app.config['SECRET_KEY'] = 'temporary-secret-key'
    
    @app.route('/')
    def index():
        return "AdTrack Investor Presentation Website - Coming Soon!"
    
    return app
