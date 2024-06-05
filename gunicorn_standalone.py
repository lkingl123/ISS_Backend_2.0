from gunicorn.app.base import BaseApplication
from app import server

import multiprocessing  # Import the multiprocessing module


def number_of_workers():
    # Let's define the number of workers as twice the number of CPU cores + 1
    return (multiprocessing.cpu_count() * 2) + 1


class StandaloneApplication(BaseApplication):
    # Here, StandaloneApplication is a new class you're defining. It's a subclass of BaseApplication, not a superclass.
    # Subclassing means StandaloneApplication inherits methods and properties from BaseApplication and can also have its own unique methods and properties.

    def __init__(self, app, options=None):
        # Correct, __init__ is the constructor method in Python. It's called when you create an instance of this class.
        # 'self' refers to the instance itself, 'app' is the Flask application, and 'options' are Gunicorn configurations.
        self.options = options or {}
        # This sets self.options to the provided options dict or an empty dict if none were provided.
        self.application = app
        # This stores the Flask app in this instance for later use.
        # super(StandaloneApplication, self).__init__()
        super().__init__()
        # This line calls the __init__ method of the superclass (BaseApplication) to ensure it's also initialized properly.

    def load_config(self):
        # This method overrides a BaseApplication method to provide custom configuration.
        config = {
            key: value
            for key, value in self.options.items()
            if key in self.cfg.settings and value is not None
        }
        # This creates a dictionary of configuration options that are actually allowed by Gunicorn and are not None.
        for key, value in config.items():
            self.cfg.set(key.lower(), value)
            # This loop sets each configuration option in the Gunicorn configuration.

    def load(self):
        # This method overrides a BaseApplication method to load the application.
        return self.application
        # It returns the Flask application to be run by Gunicorn.


if __name__ == "__main__":
    options = {
        "bind": "%s:%s" % ("0.0.0.0", "8050"),
        "workers": number_of_workers(),  # Call the function to set the number of workers dynamically
    }
    # Replace 'app' with your actual Flask app instance
    StandaloneApplication(server, options).run()

