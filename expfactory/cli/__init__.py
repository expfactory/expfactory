#!/usr/bin/env python

'''
client initialization: part of expfactory package

Copyright (c) 2017, Vanessa Sochat
All rights reserved.

Redistribution and use in source and binary forms, with or without
modification, are permitted provided that the following conditions are met:

* Redistributions of source code must retain the above copyright notice, this
  list of conditions and the following disclaimer.

* Redistributions in binary form must reproduce the above copyright notice,
  this list of conditions and the following disclaimer in the documentation
  and/or other materials provided with the distribution.

* Neither the name of the copyright holder nor the names of its
  contributors may be used to endorse or promote products derived from
  this software without specific prior written permission.

THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

'''

from glob import glob
import argparse
import sys
import os


def get_parser():

    parser = argparse.ArgumentParser(
    description="expfactory: produce a reproducible battery of container experiments")


    subparsers = parser.add_subparsers(help='Experiment Factory actions',
                                       title='actions',
                                       description='actions for expfactory tools',
                                       dest="command")


    # List
    listy = subparsers.add_parser("list", 
                                   help="List available Expfactory Experiments from Github")

    # Install
    install = subparsers.add_parser("install", 
                                     help="install an Experiment from Github")

    install.add_argument('src', nargs=1, help='source url or folder of experiment')
    install.add_argument("--folder", dest='folder', 
                          help="empty folder to install experiment, defaults to pwd", 
                          type=str, default=None)

    install.add_argument('--force', '-f',dest="force",
                         help="force installation into non empty directory",
                         default=False, action='store_true')


    # Experiments and Runtime Config
    parser.add_argument("--experiments", dest='experiments', 
                         help="comma separated list of experiments for a local battery", 
                         type=str, default=None)

    parser.add_argument("--subid", dest='subid', 
                         help="subject id for saving database",
                         type=str, default=None)

    parser.add_argument('--no-random', dest="disable_randomize",
                         help="present experiments serially",
                         default=True, action='store_false')

    # Server variables that likely don't need to be changed
    parser.add_argument("--time", dest='time',
                         help="maximum number of minutes for battery to endure, to select experiments",
                         type=int, default=99999)

    parser.add_argument("--base", dest='base', 
                         help="experiments base (default /scif/apps)",
                         type=str, default=None)

    return parser


def get_subparsers(parser):
    '''get a dictionary of subparsers to help with printing help
    '''
    actions = [action for action in parser._actions 
               if isinstance(action, argparse._SubParsersAction)]

    subparsers = dict()
    for action in actions:
        # get all subparsers and print help
        for choice, subparser in action.choices.items():
            subparsers[choice] = subparser

    return subparsers


def main():

    from expfactory.logger import bot
    from expfactory.version import __version__
    bot.info("Expfactory Version: %s" % __version__)

    parser = get_parser()
    subparsers = get_subparsers(parser)

    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    # Does the use want to install?
    command = args.command
    if command == "install":
        from .install import main

    elif command == "list":
        from .list import main

    # No argument supplied
    else:

        # A base exists for experiments
        base = os.environ.get('EXPFACTORY_BASE')
        if args.base is not None or base is not None:
            from .main import main
            command = "main"
        else:
            command = "list"
            from .list import main

    # Pass on to the correct parser
    if command is not None:

        # Main doesn't have a subparser
        subparser = None
        if command != "main":
            subparser = subparsers[command]

        main(args=args,
             parser=parser,
             subparser=subparser)


if __name__ == '__main__':
    main()
