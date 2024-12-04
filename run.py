import sys
import os
from app import create_app

# Add the `src` folder to the Python path
sys.path.append(os.path.join(os.path.dirname(__file__), "src"))
app = create_app()

if __name__ == "__main__":
    app.run(debug=True)
