# Flask-Webapp
Web app for data exploration functionality via airpartners.org

Structured and managed by Miles Mezaki, Air Partners associate.
Tools created by Ian Eykamp, Neel Dhulipala, Andrew DeCandia, Lauren Xiong and other Air Partners associates.

# Requirements #

### Install a Virtual Environment ###

To run the webapp in development mode, you will need to have a working version of Python 3, which you can install from the anaconda website. A virtual environment for package management is preferred. To create a virtual environment, first globally install virtualenv:

`python3 -m pip install --user virtualenv`

and then create a virtual environment:

`python3 -m venv env`

This will create a virtual environment (extra repository with static python information, like packages and version) called "env". Virtual environments are important to prevent version conflicts for different packages. If a developer is working on one project that requires Pandas 1.1.2 and another project that requires Pandas 1.2.7, they will need to constantly install different packages to run different software bundles. Similarly, if one program was written in Python 3.10 while another was written in Python 3.9.7, certain features may be unrunnable with one version or another. That is the rationale behind localized package and version management.

### Install Dependencies ### 
To install the packages used in this project, which are detailed in `requirements.txt`, use the following command:

`pip install -r requirements.txt`

If making updates to the repository and you want to copy over new dependencies to the requirements.txt file, use

`pip freeze > requirements.txt`

### Create a Path Variable for Flask ###

`wsgi.py` and `app.py` are reserved names and Flask will automatically recognize them if you type

`flask run`

A safe way of ensuring Flask will run them is by exporting a path variable with the name of the Python app file. Suppose `wsgi.py`, which runs the app, were actually called `hello.py`. Then the following would be the terminal (Bash) command to run:

`export FLASK_APP=hello`

Do **NOT** change the name of the run file to `flask.py`. This will conflict with Flask's framework itself.

As mentioned before, type

`flask run` and navigate to the port/socket 5000, which Flask uses by default for its servers.

# Querying Quant-AQ API #

To have the app fully functional, it is necessary to query the Quant-AQ database for information from sensors in the field. Navigate to https://www.quant-aq.com/api-keys and generate an API key for your personal use. Do **not** push this key to GitHub or any online sources. Save this key in a document called `quantaq-key.py` as follows:

`QUANTAQ_APIKEY = '39203_YOUR_KEY_F9070'`

This should be enough for the existing code to access the Quant-AQ API.

# File Catalog #

`__init__.py` indicates to Python that this folder is treated as a package and is standard for shipping code modules.
This does not change much, but allows imports to be cleaner and in this case makes only one or two files really critical to understand how the app is being run. One notable change that initializing a package comes with is the need for a `.` before any import in the same folder. If importing from `quantaq_key.py`, for example, I would say:

`from .quantaq_key import QUANTAQ_KEY`

instead of the usual

`from quantaq_key`

There are two packages in this repository: `src` and `data-exploration-tool`.

# Deployment #


