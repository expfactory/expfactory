
/* ************************************ */
/* Define helper functions */
/* ************************************ */
function getDisplayElement () {
    $('<div class = display_stage_background></div>').appendTo('body')
    return $('<div class = display_stage></div>').appendTo('body')
}

/* ************************************ */
/* Define experimental variables */
/* ************************************ */
var experiment_len = 3
var gap = 0
var current_trial = 0
var stim = '<div class = "shapebox"><div id = "cross"></div></div>'
var rts = []
var avg_rt = 0
var reject = false

/* ************************************ */
/* Set up jsPsych blocks */
/* ************************************ */
/* define static blocks */

var end_block = {
  type: 'poldrack-text',
  timing_response: 60000,
  text: '<div class = centerbox><p class = center-block-text>Thanks for completing this task!</p><p class = center-block-text>Press <strong>enter</strong> to continue.</p></div>',
  cont_key: [13],
  timing_post_trial: 0
};

/* define test block */
var test_block = {
  type: 'poldrack-single-stim',
  stimulus: stim,
  is_html: true,
  data: {exp_id: "test_task", trial_id: "test"},
  choices: [32],
  timing_post_trial: 100,
  on_finish: function(data) {
    rts.push(data.rt)
    var total = 0;
    for(var i = 0; i < rts.length; i++) {
        total += rts[i];
    }
    avg_rt = total / rts.length
    if (avg_rt < 100) {
      reject = true
    } else {
      reject = false
    }
  }
}

/* create experiment definition array */
var test_task_experiment = [];
for (var i = 0; i < experiment_len; i++) {
  test_task_experiment.push(test_block);
}
test_task_experiment.push(end_block);
