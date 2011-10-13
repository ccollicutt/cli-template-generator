#!/usr/bin/python

import re
import sys
import os, os.path
import ConfigParser

try:
    from Cheetah.Template import Template
except ImportError:
    print >>sys.stderr, 'ERROR: kicker requires Cheetah templates'
    sys.exit(1)

try:
    import argparse
except ImportError:
    print >>sys.stderr, 'ERROR: kicker requires argparse'
    sys.exit(1)

CONFIG_FILE = "./skeleton.conf"
TEMPLATE="./skeleton.tpl"

def main(args):
    
    # Much of the argparse/configparser parts taken from 
    # http://blog.vwelch.com/2011/04/combining-configparser-and-argparse.html

    conf_parser = argparse.ArgumentParser(
        # Turn off help, so we print all options in response to -h
        add_help=False
    )

    conf_parser.add_argument(
        "-c", "--config-file", 
        dest="configfile", 
        help="Use a different config file than %s" % CONFIG_FILE
    )

    args, remaining_argv = conf_parser.parse_known_args()

    if args.configfile:
        configfile = args.configfile
    else:
        configfile = CONFIG_FILE

    # Make sure the configfile is a file
    if not os.path.isfile(configfile):
        print >>sys.stderr, 'ERROR: %s is not a file' % configfile
        sys.exit(1)

    config = ConfigParser.SafeConfigParser()
    try:
        config.read([configfile])
    except:
        print >>sys.stderr, 'ERROR: There is an error in the config file'
        sys.exit(1)

    defaults = dict(config.items("default"))

    parser = argparse.ArgumentParser(
        # Inherit options from config_parser
        parents=[conf_parser],
        # print script description with -h/--help
        description=__doc__,
        # Don't mess with format of description
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )

    parser.set_defaults(**defaults)

    #---------------------------------------------------------------------------
    # Add more arguments here!
    #
    # Eg.
    #
    #   parser.add_argument(
    #    "-s", "--somearg", 
    #    dest="somearg", 
    #    help="Replace this with a real argument!"
    #)

    parser.add_argument(
        "--hello", 
        dest="hello", 
        help="Who are you saying hello to?"
    )

    #
    # Done with arguments
    #---------------------------------------------------------------------------

    # Capture args
    args = parser.parse_args(remaining_argv)

    # Makes args into a dictionary to feed to searchList
    d = args.__dict__

    # Create template object
    # - the searchList=[d] is the best!
    t = Template(file=TEMPLATE, searchList=[d])

    print(t.respond())
    sys.exit(0)
    
if __name__ == '__main__':
    main(sys.argv)
