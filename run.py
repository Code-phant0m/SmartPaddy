import sys
import os
from app import create_app

# Add the `src` folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
app = create_app()

if __name__ == "__main__":
    if app:
        port = int(os.environ.get("PORT", 8080))
        app.run(port=port, host='0.0.0.0')
    else:
         print("Failed to initialize the application.")
