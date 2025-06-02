import os
import sys
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))  # DON'T CHANGE THIS !!!

from src import create_app

app = create_app()

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
