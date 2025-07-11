from flask import Flask
from routes.main_routes import main
from routes.admin_routes import admin_bp
from routes.pharma_routes import pharma_bp
from routes.manager_routes import manager_bp
from routes.reception import reception_bp

app = Flask(__name__)
app.register_blueprint(main)
app.register_blueprint(admin_bp)
app.register_blueprint(pharma_bp)
app.register_blueprint(manager_bp)
app.register_blueprint(reception_bp)
app.secret_key = '3e0f3c75113e4ee46b8a287b97b5def1'



@app.after_request
def add_no_cache_headers(response):
    response.headers['Cache-Control'] = 'no-store, no-cache, must-revalidate, private, max-age=0'
    response.headers['Pragma'] = 'no-cache'
    response.headers['Expires'] = '0'
    return response

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')


