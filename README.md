# pysipgate

## What is this?

This project consists of a high level Python API for the
[http://www.sipgate.de/basic/api](Sipgate basic API) and a GUI which is based
around a tray icon using this API.

The GUI offers the following features:

* initiate voice calls
* detect phone numbers from clipboard
* show account balance

## Setup

There is a `setup.py` for automated installation. To install `pysipgate` simply
call:

    ./setup.py install --user

The GUI is configured in the file `~/.pysipgate`. It should look like this:

    [account]
    user: thammi
    password: 123456

