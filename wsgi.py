"""
wsgi.py — WSGI production entrypoint for Render, Railway, Heroku, etc.
"""
import config
from dashboard import app, init_api_model

# Pre-train / load the model into memory upon server startup
init_api_model()

if __name__ == "__main__":
    app.run(host=config.HOST, port=config.PORT, debug=config.DEBUG)
