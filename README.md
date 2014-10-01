schemePy & Holodeck
===================

Installation Notes
------------------

schemePy with the holodeck webfrontend (`app.py`)requires python version 3.4 to be installed. It does not work with python2.7 or below!

    $ python3 --version
    Python 3.4.1

Sadly, Debian based software repositories currently only provide binaries for python 3.3. This is enough to run the schemepy repl (`repl.py`).

If you want to use the webfrontend as well, please install python3.4 from the offical python homepage[1].
Afterwards you need to install the flask framework for python3:

If you are using an virtualenv

    python3 -m pip install flask

otherwise:

    sudo python3 -m pip install flask









[1]: https://www.python.org/download/
