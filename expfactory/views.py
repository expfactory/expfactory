'''
views.py: part of expfactory package

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

from flask import (
    flash,
    render_template, 
    request, 
    redirect,
    session
)

from flask_wtf.csrf import generate_csrf
from flask_cors import cross_origin
from expfactory.logman import bot
from werkzeug import secure_filename
from expfactory.utils import (
    convert2boolean, 
    getenv,
    get_post_fields
)


from expfactory.database import generate_subid
from expfactory.server import app
from random import choice
import os

from expfactory.forms import ParticipantForm


# SECURITY #####################################################################

@app.after_request
def inject_csrf_token(response):
    response.headers.set('X-CSRF-Token', generate_csrf())
    return response
  

# EXPERIMENT PORTAL ############################################################

@app.route('/experiments')
def experiment_base():
    return render_template('experiments/index.html')


# Home portal to start experiments
@app.route('/', methods=['GET', 'POST'])
def home():

    form = ParticipantForm()

    if request.method == "POST":   

        print('SESSION')
        print(session)
        # Submit and valid
        if form.validate_on_submit():
            session['username'] = form.openid.data
            session['experiments'] = form.exp_ids.data.split(',') # list
            flash('Participant ID: "%s", Experiments: %s' %
                  (form.openid.data,
                  str(form.exp_ids.data)))
            return redirect('/start')

        # Submit but not valid
        return render_template('portal/index.html', experiments=app.lookup,
                                                    base=app.base,
                                                    form=form, toggleform=True)

    # Not submit
    return render_template('portal/index.html', experiments=app.lookup,
                                                base=app.base,
                                                form=form)


# EXPERIMENT ROUTER ############################################################


@app.route('/next', methods=['POST', 'GET'])
def next():
    print(request)
    if request.method == 'POST':
        fields = get_post_fields(request)
        result_file = save_data(session, fields)
        print(result_file)

    username = session.get('username')
    if username is None:
        flash('You must start a session before doing experiments.')
        return redirect('/')

    experiment = app.get_next(session)
    if experiment is None:
        flash('Congratulations, you have finished the battery!')
        return redirect('/finish')

    return redirect('http://127.0.0.1/experiments/%s' %experiment)


# Reset/Logout
@app.route('/logout', methods=['POST', 'GET'])
def logout():

    # If the user has finished, clear session
    del session['expfactory_subid']
    del session['username']
    del session['experiments']
    return redirect('/')


# Finish
@app.route('/finish', methods=['POST', 'GET'])
def finish():

    # If the user has finished, clear session
    del session['expfactory_subid']
    del session['username']
    del session['experiments']

    #TODO: need to handle POST with CSRF, document standard post
    # create local result database and option to use "real" db - both
    # should be easy to do / switch based on environment setting.
    return render_template('finish/index.html')



@app.route('/start')
def start():
    '''start a battery.
    '''
    username = session.get('username')
    if username is None:
        flash('You must start a session before doing experiments.')
        return redirect('/')

    # If the user hasn't started, assign new subid
    if not session.get('expfactory_subid'):
        session['expfactory_subid'] = generate_subid()

    print('SESSION')
    print(session)
    print(request.headers)
    return render_template('start/index.html')


# Route the user to the next experiment
def battery_router(request,bid,eid=None,userid=None,no_send=False):
    '''battery_router will direct the user (determined from the session variable) to an uncompleted experiment. If an
    experiment id is provided, the redirect is being sent from a completed experiment, and we log the experiment as completed
    first. 
    :param bid: the battery id
    :param eid: the experiment id, if provided, means we are submitting a result
    :param userid: the userid, will be "DUMMY" if doing a battery preview
    :param no_send: don't send result to email, default is False
    '''
    # No robots allowed!
    if request.user_agent.is_bot:
        return render_to_response("messages/robot_sorry.html")

    # Is this a valid user?
    preview = False
    if userid != "DUMMY": # not a preview battery
        userid = request.session.get('worker_id', None)
        if userid == None:
            return render_to_response("messages/invalid_id_sorry.html")
    else:
        # If no_send is defined, then don't send
        preview = True
        no_send = request.session.get('no_send', False)
    
    worker = get_worker(userid)

    # Retrieve the battery based on the bid
    battery = get_battery(bid,request)

    # If there is a post, we are finishing an experiment and sending data
    if request.method == "POST" and eid != None:

        experiment = get_experiment(eid,request)
   
        # If it's a survey, format the results before sending
        data = request.POST

        if experiment.template == "survey":
            data = complete_survey_result(experiment,data)
        
        else:
            data = dict(data)

        # Mark the experiment as completed    
        if experiment not in worker.experiments_completed.all():

            # Only send data if the user hasn't completed it yet
            if no_send != True:
                send_result.apply_async([experiment.id,worker.id,data])
            worker.experiments_completed.add(experiment)
            worker.save()

    # Deploy the next experiment
    missing_batteries, blocking_batteries = check_battery_dependencies(battery, worker)
    if missing_batteries or blocking_batteries:
        return render_to_response(
            "messages/battery_requirements_not_met.html",
            context={'missing_batteries': missing_batteries,
                     'blocking_batteries': blocking_batteries}
        )

    # Is the battery still active?
    if battery.active == False:
        context = {"contact_email":battery.email}
        return render(request, "messages/battery_inactive.html", context)

    # Does the worker have experiments remaining?
    uncompleted_experiments = get_worker_experiments(worker,battery)
    experiments_left = len(uncompleted_experiments)
    if experiments_left == 0:
        # If it's a preview, reset it before showing the final page
        if preview == True:
            reset_preview(request,bid,redirect=False)
        # Thank you for your participation - no more experiments!
        return render_to_response("messages/worker_sorry.html")

    next_experiment = select_experiments(battery,uncompleted_experiments)[0]
    
    # Redirect the user to the experiment!
    return HttpResponseRedirect(next_experiment.serve_url())







################################################################################
# OLD VIEWS ####################################################################
################################################################################


def get_field(request,fields,value):
    """
    Get value from a form field

    """
    if value in request.form.values():
        fields[value] = request.form[value]
    return fields


# INTERACTIVE BATTERY GENERATION ####################################################
# Step 0: User is presented with base interface
@app.route('/battery')
def battery():
    return render_template('battery.html')

# STEP 1: Validation of user input for battery
@app.route('/battery/validate',methods=['POST'])
def validate():
    logo = None
    if request.method == 'POST':
        fields = dict()
        for field,value in request.form.iteritems():
            if field == "dbsetupchoice":
                dbsetupchoice = value
            else:
                fields[field] = value

        # DATABASE SETUP ###################################################
        # If the user wants to generate a custom database:
        if dbsetupchoice == "manual":

            # Generate a database url from the inputs
            fields["database_url"] =  generate_database_url(dbtype=fields["dbtype"],
                                                 username=fields["dbusername"],
                                                 password=fields["dbpassword"],
                                                 host=fields["dbhost"],
                                                 table=fields["dbtable"]) 
        else:
            # If generating a folder, use sqlite3
            if fields["deploychoice"] == "folder":
                fields["database_url"] = generate_database_url(template="sqlite3")       
            # Otherwise, use postgres
            else: 
                fields["database_url"] = generate_database_url(template="mysql")       
        
        # LOCAL FOLDER #####################################################
        if fields["deploychoice"] == "folder":

            # Copy the custom logo
            if "file" in request.files and allowed_file(request.files["file"]):
                logo = secure_filename(request.files["file"])
                add_custom_logo(battery_repo="%s/battery" %(app.tmpdir),logo=logo)
    
            # Generate battery folder with config file with parameters
            generate_config("%s/battery" %(app.tmpdir),fields)

        else: 
            prepare_vm(battery_dest=app.tmpdir,fields=fields,vm_type=fields["deploychoice"])

        # Get valid experiments to present to user
        valid_experiments = [{"exp_id":e[0]["exp_id"],"name":e[0]["name"]} for e in app.experiments]

        return render_template('experiments.html',
                                experiments=str(valid_experiments),
                                this_many=len(valid_experiments),
                                deploychoice=fields["deploychoice"])

    return render_template('battery.html')

# STEP 2: User must select experiments
@app.route('/battery/select',methods=['POST'])
def select():
    if request.method == 'POST':
        fields = dict()
        for field,value in request.form.iteritems():
            if field == "deploychoice":
                deploychoice = value
            else:
                fields[field] = value

        # Retrieve experiment folders 
        valid_experiments = app.experiments
        experiments =  [x[0]["exp_id"] for x in valid_experiments]
        selected_experiments = [x for x in fields.values() if x in experiments]
        experiment_folders = ["%s/experiments/%s" %(app.tmpdir,x) for x in selected_experiments]

        # Option 1: A folder on the local machine
        if deploychoice == "folder":

            # Add to the battery
            generate(battery_dest="%s/expfactory-battery"%app.tmpdir,
                     battery_repo="%s/battery"%app.tmpdir,
                     experiment_repo="%s/experiments"%app.tmpdir,
                     experiments=experiment_folders,
                     make_config=False,
                     warning=False)

            battery_dest = "%s/expfactory-battery" %(app.tmpdir)

        # Option 2 or 3: Virtual machine (vagrant) or cloud (aws)
        else:
            specify_experiments(battery_dest=app.tmpdir,experiments=selected_experiments)
            battery_dest = app.tmpdir 

        # Clean up
        clean_up("%s/experiments"%(app.tmpdir))
        clean_up("%s/battery"%(app.tmpdir))
        clean_up("%s/vm"%(app.tmpdir))        

        return render_template('complete.html',battery_dest=battery_dest)

def clean_up(dirpath):
    if os.path.exists(dirpath):
        shutil.rmtree(dirpath)
