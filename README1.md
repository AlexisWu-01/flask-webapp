# Flask-Webapp
Web app for data exploration functionality via webapp. airpartners.org

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

Upon creation of this document, this webapp is meant to be deployed on Linode. If this has changed, or if Linode services were in some way updated, this guide may not be 100% accurate.

To follow along and do any server maintenance, you can ssh in or log in through Linode's console. I usually ssh in. First get the IP address of the server, then run `ssh root@(ip)`. **Note: You will NOT be able to ssh in with the Symantec Endpoint Protection firewall enabled.** 

**You will have to press `WIN + R` and run `smc -stop`.**

### Create the Linode ###

First I will walk through the process of setting up a server for the first time, should it be necessary.

In the cloud manager, you will be able to access all Linode servers belonging to the airpartners account (hopefully just one). In creating the current Linode, I selected Nanode as our storage needs are not extreme yet. This may change. The server is running on an Ubuntu 20.04 image.

### Installing Dependencies ###

Similar to how your own computer needs Python to run Flask, it is first necessary to install Python and configure Git to retrieve the webapp repository.

#### Configuring Git ####

You will want to configure Git to attempt to connect to GitHub using your username and password. Luckily, Git makes this relatively easy for us:

`git config --global user.name "mlsmzk"`
`git config --global user.email mlsmzk02@gmail.com`

To check for spelling errors, use `git config --list`.

Sample output:
user.name=mlsmzk
user.email=mlsmzk02@gmail.com

Next we will want to add an SSH key to the agent so that Git knows we are the owner of the account. To do this, you can follow Git's guide online, or follow steps highlighted below.

1. In the terminal, you can generate an SSH key with `ssh-keygen -t ed25519 -C "your_email@example.com"` and save everything in the default location. Overwriting is up to you, since it will probably only kick out past Air Partners students. If you choose not to overwrite and to save in a new location, note that you will have to tell Git to look in that location for your SSH key with a different filename in step 2.
2. Run `ssh-add ~/.ssh/id_ed25519` (or whatever the file you saved the key in is called).
3. Finally, go to GitHub in a browser, enter your settings -> SSH and GPG Keys -> Add a new SSH key. In the server's terminal, type `cat ~/.ssh/id_ed25519.pub` and copy the output into GitHub.

Now you should be able to clone the repository into the server!

#### Get Python and Updates ####

Though this could have been done before configuring Git, this order is perfectly fine as well. Start by running
`apt-get update && apt-get upgrade` (might need sudo if you're not root user). This will retrieve any updates the system needs and is just good practice to do.

Next, run `sudo apt install software-properties-common`, which I believe installs packages that Python uses to build itself, or uses for other purposes. Then tell the computer that we want another default repository to check for updates and upgrades for: `sudo add-apt-repository ppa:deadsnakes/ppa`.

With these preliminary steps done, all you need to do is run `sudo apt install python3.9`. Note that Python 3.9+ is important since certain features were used that are reliant on 3.9 syntax. It does not work for 3.8 or lower. Check the version of Python running as default on the machine. It should say Python 3.9, but it might say Python 3.8. You can check with `python -V`. As of the writing of this, the server for some reason defaults to installing Python 3.8 and will throw errors if you try to run the webapp without creating a virtual environment with Python 3.9 or higher. Since virtual environments create instances of Python with the version used in their inception, we first need to make sure the python version used to instantiate the venv is Python 3.9+. We can do this by updating python alternatives.

1. **If your Python version is less recent than Python 3.9**, run `sudo update-alternatives --install /usr/bin/python python /usr/bin/python3.9 1`. Now check `python -V`, which should say Python3.9. Assuming it does, you can now start installing required packages!
2. If you haven't already, you can `apt install python3-pip`. I'm not entirely sure which pip it will install with, nor if it should be python3-pip or python-pip. Once pip is installed, the rest is very easy.
3. Install the virtual environment package. This should come with Python, but didn't for me. Run the command `sudo apt install python3-venv`. Now try creating a virtual environment by navigating to the webapp's directory and then doing `python -m venv venv`. With any luck, it will create a virtual environment with a good Python version; check with `python -V`.

#### Pip Installs ####

Since there is a requirements.txt, all we should need to do is get pip to download everything in the requirements.

Run `pip install -r requirements.txt` and watch the magic happen.

### Run the Server ###

Now we're hopefully able to run the server. There are certain security measures to set up that make the system safer, but Air Partners is not exactly a target for attack either. When we `flask run`, we need to add the extra flag `--host=0.0.0.0` to let Flask know we are deploying it to the internet. Now navigate to the IP and hopefully it works!

OK, so the server works. What about when you end the SSH login session? Try closing it, then accessing the same site. So why doesn't it work? When you SSH in, you are starting a session with the server, which can be thought of as a process. Anything done as a result of this process is a child process of our session, and is therefore ended when the parent itself terminates. Hence we need some sort of distinguishment for the app starting. With Node.js projects, I believe byobu or other tools are go-to. In this case, we can use `screen` or `nohup` (no hangup).

As of right now, I have chosen to use `nohup flask run --host=0.0.0.0` to maintain accessibility. This may not be the most scalable design decision, so I leave the choice to replace this with a more user-friendly alternative in the hands of my successors. Once we run this command, we can safely end the SSH session without ending the child process, meaning the webapp is now accessible.

### Make Changes to the Server Code ###

Undoubtedly there are improvements that can be made to the webapp. To do so, one can start another SSH session and pull changes from Git. There's one problem though: the nohup process doesn't depend on sessions. Thus it is still running in the background, despite us starting another SSH session. For the enthusiastic crowd, making a Bash script to solve this problem would be fairly easy. Otherwise, we can solve this problem with some manual commands.

1. Run `ps`. See that it doesn't show the background processes? We have to force it to show background processes with `ps -ef`.
2. Locate the PID (second column) of the process. You can make this easier by running `ps -ef |grep "flask run --host=0.0.0.0"`, assuming no changes have been made to the actual run command.
3. Enter `kill (PID val)`.

If you would like to write a bash script to do this for us, visit https://stackoverflow.com/questions/17385794/how-to-get-the-process-id-to-kill-a-nohup-process to learn more.

# Next Steps #

 There are a few directions the next developer could take this project.

 1. Asynchronous API calls

 There exists a Python module called AsyncIO structured to act somewhat like the JavaScript await/async format. This likely allows for `flask run` to render HTML templates while awaiting for certain Python variables to be generated. My vision of how this might look is the following:

 a. We await the QuantAQ API call and in the meantime have an empty dictionary (which will be a JSON object) to dump into our HTML document. When we `flask run`, we render the HTML template with an empty JSON, but it fills up before executing the JavaScript and loading the real-time map.

 2. Dynamic Map

 At the moment, and this is an enormous oversight on my part, the real-time map does not actually update in real-time. It would be nice if there a way to connect to sensors directly, but it is most likely that one would have to constantly be accessing the QuantAQ API to divulge information in real-time. There are two solutions, one of which I believe would be more valuable to the next developer's learning than the other. Perhaps the easier would be to synchronize the real-time map with QuantAQ's map on their website. Instead of designing Air Partners' own real-time map, allow QuantAQ to do the data gathering and us to forward that map to stakeholders. There is no need to reinvent the wheel. But if you find yourself particularly inventive, it would be both instructive and valuable to look into seeing if there is a way to reboot the server every *n* timesteps. Whenever the server is started is when the API call is made, and afterwards information is not updated. In order to fix this, it would be prudent to look into a periodic server restart at reasonable time intervals, like every hour, maybe every three hours.
