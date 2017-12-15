/* ************************************ */
/* Define helper functions */
/* ************************************ */
function evalAttentionChecks() {
  var check_percent = 1
  if (run_attention_checks) {
    var attention_check_trials = jsPsych.data.getTrialsOfType('attention-check')
    var checks_passed = 0
    for (var i = 0; i < attention_check_trials.length; i++) {
      if (attention_check_trials[i].correct === true) {
        checks_passed += 1
      }
    }
    check_percent = checks_passed / attention_check_trials.length
  }
  return check_percent
}

function assessPerformance() {
  /* Function to calculate the "credit_var", which is a boolean used to
  credit individual experiments in expfactory. 
   */
  var experiment_data = jsPsych.data.getTrialsOfType('poldrack-single-stim')
  var missed_count = 0
  var trial_count = 0
  var rt_array = []
  var rt = 0
  for (var i = 0; i < experiment_data.length; i++) {
    trial_count += 1
    rt = experiment_data[i].rt
    key = experiment_data[i].key_press
    if (rt == -1) {
      missed_count += 1
    } else {
      rt_array.push(rt)
    }

  }
  //calculate average rt
  var avg_rt = -1
  if (rt_array.length !== 0) {
    avg_rt = math.median(rt_array)
  } 
  var missed_percent = missed_count/trial_count
  credit_var = (missed_percent < 0.4 && avg_rt > 200)
  if (credit_var === true) {
      performance_var = Math.max(0, 1000 - avg_rt)
  } else {
      performance_var = 0
  }

  jsPsych.data.addDataToLastTrial({"credit_var": credit_var,"performance_var": performance_var})
}


/* ************************************ */
/* Define experimental variables */
/* ************************************ */
// generic task variables
var run_attention_checks = false
var attention_check_thresh = 0.65

// task specific variables
var experiment_len = 3
var gap = 0
var current_trial = 0
var stim = '<div class = "shapebox"><div id = "cross"></div></div>'
var credit_var = true
var performance_var = 0

/* ************************************ */
/* Set up jsPsych blocks */
/* ************************************ */

// Set up attention check node
var attention_check_block = {
  type: 'attention-check',
  timing_response: 180000,
  response_ends_trial: true,
  timing_post_trial: 200
}

var attention_node = {
  timeline: [attention_check_block],
  conditional_function: function() {
    return run_attention_checks
  }
}

var add_data = {
  type: 'call-function',
  func: function() {
    jsPsych.data.addDataToLastTrial({'added_Data?': 'success!'})
  }
}

//Set up post task questionnaire
var post_task_block = {
   type: 'survey-text',
   data: {
       trial_id: "post task questions"
   },
   questions: ['<p class = center-block-text style = "font-size: 20px">Please summarize what you were asked to do in this task.</p>',
              '<p class = center-block-text style = "font-size: 20px">Do you have any comments about this task?</p>'],
   rows: [15, 15],
   columns: [60,60],
};

/* define static blocks */
var end_block = {
  type: 'poldrack-text',
  data: {
    trial_id: 'end',
    exp_id: 'test_task'
  },
  timing_response: 180000,
  text: '<div class = centerbox><p class = center-block-text>Thanks for completing this task!</p><p class = center-block-text>Press <strong>enter</strong> to continue.</p></div>',
  cont_key: [13],
  timing_post_trial: 0,
  on_finish: assessPerformance
}

/* define test block */
var test_block = {
  type: 'poldrack-single-stim',
  stimulus: stim,
  is_html: true,
  data: {
    trial_id: "test"
  },
  choices: [32],
  timing_response: 2000,
  timing_post_trial: 100,
  on_finish: function() {
    jsPsych.data.addDataToLastTrial({'addingOnTrial': 'added!'})
  }
}

/* create experiment definition array */
var test_task_experiment = [];
for (var i = 0; i < experiment_len; i++) {
  test_task_experiment.push(test_block);
}
test_task_experiment.push(add_data)
test_task_experiment.push(attention_node)
test_task_experiment.push(post_task_block)
test_task_experiment.push(end_block);