from optparse import OptionParser
from pysipgate.sipgate import *
import os.path
import sys

DEFAULT_CONFIG_FILE = "~/.pysipgate"

def main():
    parser = OptionParser()
    parser.add_option("-f", "--file", dest="filename",
            help="Use configuration file", metavar="FILE")
    parser.add_option("-s", "--sms",
            help="Send an SMS", metavar="NUMBER")
    parser.add_option("-c", "--call",
            help="Initiate a phone call", metavar="NUMBER")

    (options, args) = parser.parse_args()

    if options.filename:
        config_file = options.filename
    else:
        config_file = DEFAULT_CONFIG_FILE

    if not any([options.sms, options.call]):
        from pysipgate import gui
        gui.start(config_file)
    else:
        try:
            con = connection_from_config(config_file)

            if options.sms:
                text = sys.stdin.read()
                print("Sending SMS ...")
                con.text(options.sms, text)
            elif options.call:
                print("Initiating voice call ...")
                con.voice(options.call)
        except SipgateAuthException:
            msg = "Could not authenticate with Sipgate server. Please adjust your account settings in '%s'" % config_file
            print(msg)
            return 1
        except SipgateException as err:
            print(err)
            return 1

if __name__ == '__main__':
    sys.exit(main())
