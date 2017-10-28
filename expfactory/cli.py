#!/usr/bin/env python

'''
cli.py: part of expfactory package

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

    parser.add_argument("--list", dest='list',  # TODO: this will list from library
                         help="list available experiments.",   
                         default=False, action='store_true')

    parser.add_argument("--experiments", dest='experiments', 
                         help="comma separated list of experiments for a local battery", 
                         type=str, default=None)

    parser.add_argument("--subid", dest='subid', 
                         help="subject id for saving database",
                         type=str, default=None)

    parser.add_argument("--base", dest='base', 
                         help="base folder with experiment subfolders (defaults to /scif/apps)",
                         type=str, default='/scif/apps')

    parser.add_argument("--port", dest='port', 
                         help="port to preview experiment", 
                         type=int, default=None)

    parser.add_argument("--time", dest='time',
                         help="maximum number of minutes for battery to endure, to select experiments",
                         type=int, default=99999)

    parser.add_argument('--run', dest="run",
                         help="run a single experiment/survey or battery locally",
                         default=False, action='store_true')

    return parser


def main():

    from expfactory.logman import bot
    # This will also import and set defaults

    parser = get_parser()

    try:
        args = parser.parse_args()
    except:
        parser.print_help()
        sys.exit(0)


    # Export environment variables for the client
    experiments = args.experiments
    if experiments is None:
        experiments = " ".join(glob("%s/*" %args.base))

    os.environ['EXPERIMENTS'] = experiments

    # Does the base folder exist?
    if not os.path.exists(args.base):
        bot.error("Base folder %s does not exist." %args.base)
        sys.exit(1)

    os.environ['EXPFACTORY_BASE'] = args.base
    os.environ['EXPFACTORY_SUBID'] = args.subid

    from expfactory.server import start
    start(port=args.port)

if __name__ == '__main__':
    main()
