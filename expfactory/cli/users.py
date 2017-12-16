'''

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

from expfactory.logger import bot
from expfactory.defaults import EXPFACTORY_DATABASE
import sys
import os


def main(args, parser, subparser):
      
    from expfactory.server import app
    header = 'DATABASE\tTOKEN' 

    # The user wants to list active subjects
    if args.list is True:
        users = app.list_users() # returns id\ttoken
        sys.exit(0)

    # The user wants to add new subjects
    number = args.new
    if number is not None:
        print(header)
        for i in range(number):
            user = app.generate_user()
            app.print_user(user)
        sys.exit(0)

    # The user wants to manage user token
    action = None
    if args.revoke is not None:
        subid = clean(args.revoke)
        func = app.revoke_token
        action = "Revoking"
    elif args.refresh is not None:
        subid = clean(args.refresh)
        func = app.refresh_token
        action = "Refreshing"
    elif args.restart is not None:
        subid = clean(args.restart)
        func = app.restart_user
        action = "Restarting"
    elif args.finish is not None:
        subid = clean(args.finish)
        action = "Finishing"
        func = app.finish_user

    # Perform the action
    if action is not None:
        bot.info('%s %s' %(action, subid))
        result = func(subid=subid)
        if result is not None:
            print("[%s] %s --> %s" %(action.lower(), 
                                     subid,
                                     result))
        else:
            print("[%s] not successful. See logs for details." %(action.lower()))
            print("Commands may only possible for [active] status.")

        sys.exit(0)

    print('See expfactory users --help for usage')


def clean(subid):
    '''clean a subid, removing any folder extensions (_revoked or _finished)
       for the functions
    '''
    for ext in ['_revoked','_revoked']:
        subid = subid.replace(ext,'')
    return subid
