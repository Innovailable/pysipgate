# pysipgate

## What is this?

This project consists of a high level Python API for the
[http://www.sipgate.de/basic/api](Sipgate basic API) and a GUI which is based
around a tray icon using this API.

The GUI offers the following features:

* initiate voice calls
* detect phone numbers from clipboard
* SMS functionality
* show account balance

## Setup

There is a `setup.py` for automated installation. To install `pysipgate` simply
call:

    ./setup.py install --user

The GUI is configured in the file `~/.pysipgate`. It should look like this:

    [account]
    user: thammi
    password: 123456

## Usage

To use the GUI (which is based around a tray icon) simply call

    pysipgate

There are also some command line options. You can send an SMS with one simple comand

    echo "Hello World!" | pysipgate --sms 49123456789

To initiate a voice call from the command line run

   pysipgate --call 0123456789

## Bugs/TODOs

* SMS need a phone number with national area code

