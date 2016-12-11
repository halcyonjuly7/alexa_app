from project import create_app
import os

parent_dir = os.path.dirname(os.path.abspath(__file__))
config_path = os.path.join(parent_dir, "config", "config.py")


app = create_app(config_path)
if __name__ == "__main__":
    app.run(debug=True)