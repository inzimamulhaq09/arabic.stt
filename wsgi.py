from app import app as application
import os

if __name__ == "__main__":
    # Production settings
    port = int(os.environ.get("PORT", 8000))
    application.run(host='0.0.0.0', port=port)
