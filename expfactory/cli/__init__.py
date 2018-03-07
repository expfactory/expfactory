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

    parser.add_argument("--database", dest='database', 
                        choices=['fllesystem', 'sqlite'],
                        help="database for application (default filesystem)",
                        type=str, default="filesystem")

    # Users manager
    users = subparsers.add_parser("users",
                                   help="Manager for interacting with users")

    users.add_argument('--new', dest="new",
                       help="generate new user tokens, recommended for headless runtime.",
                       default=None, type=int)

    users.add_argument('--list', dest="list",
                        help="list current tokens, for a headless install",
                        default=False, action='store_true')

    users.add_argument('--revoke', dest="revoke",
                        help="revoke token for a user id, ending the experiments",
                        default=None, type=str)

    users.add_argument('--refresh', dest="refresh",
                        help="refresh a token for a user",
                        default=None, type=str)

    users.add_argument('--restart', dest="restart",
                        help="restart a user, revoking and then refresing the token",
                        default=None, type=str)

    users.add_argument('--finish', dest="finish",
                        help="finish a user session by removing the token",
                        default=None, type=str)

    # List
    listy = subparsers.add_parser("list", 
                                   help="List available Expfactory Experiments from Github")

    # List
    logs = subparsers.add_parser("logs", 
                                 help="Print expfactory logs to terminal.")

    logs.add_argument('--tail',dest="tail",
                      help="keep the log open and update in real time.",
                      default=False, action='store_true')

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

    install.add_argument("--base",'-b', dest='base', 
                         help="expfactory install base (defaults to application base)",
                         type=str, default=None)


    # Generate Build Recipe
    build = subparsers.add_parser("build", 
                                   help="Build an experiment container (or just recipe)")

    build.add_argument("--output",'-o', dest='output', 
                         help="output name for Dockerfile (if you want a custom path)", 
                         type=str, required=True)

    build.add_argument("--input",'-i', dest='input', 
                         help="use custom Dockerflie template", 
                         type=str, default=None)

    build.add_argument('experiments', nargs="+",
                        help='experiments to build in image')

    build.add_argument("--studyid", dest='studyid', 
                        help="study id for saving database",
                        type=str, default="expfactory")


    # Experiment Runtime Arguments
    parser.add_argument("--experiments", dest='experiments', 
                         help="comma separated list of experiments for a local battery", 
                         type=str, default=None)

    parser.add_argument("--subid", dest='subid', 
                         help="subject id for saving database",
                         type=str, default=None)

    parser.add_argument("--headless", dest='headless', 
                         help="headless runtime will require generation of tokens or ids.",
                         default=False, action="store_true")

    parser.add_argument('--no-random', dest="disable_randomize",
                         help="present experiments serially",
                         default=True, action='store_false')

    parser.add_argument("--base", dest='base', 
                         help="experiments base (default /scif/apps)",
                         type=str, default=None)

    # Runtime variables
    parser.add_argument("--vars", dest='vars', 
                         help="runtime variables file to pass to experiments",
                         type=str, default=None)

    parser.add_argument("--delim", dest='delim', 
                         help="delimiter for runtime variables file.",
                         type=str, default='\t')

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

    parser = get_parser()
    subparsers = get_subparsers(parser)

    try:
        args = parser.parse_args()
    except:
        sys.exit(0)

    # Does the use want to install?
    command = args.command

    # Options that shouldn't produce output
    if command in ['users']:
        os.environ['MESSAGELEVEL'] = "0"

    if args.database is not None:
        os.environ['EXPFACTORY_DATABASE'] = args.database

    from expfactory.logger import bot
    from expfactory.version import __version__
    bot.info("Expfactory Version: %s" % __version__)

    if command == "install":
        from .install import main

    elif command == "list":
        from .list import main

    elif command == "logs":
        from .logs import main

    elif command == "users":
        from .users import main

    elif command == "build":
        from .build import main

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
