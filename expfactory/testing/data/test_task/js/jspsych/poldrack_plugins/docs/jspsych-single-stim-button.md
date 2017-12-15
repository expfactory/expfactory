# jspsych-single-stim-button plugin

plugin for displaying stimuli and getting mouse responses

## Parameters

This table lists the parameters associated with this plugin. Parameters with a default value of *undefined* must be specified. Other parameters can be left unspecified if the default value is acceptable.

Parameter | Type | Default Value | Description
----------|------|---------------|------------
stimulus | string | NA | HTML string or path to stimulus to present
button_class | string | NA | class of button to listen for. All buttons that have this class will advance the trial and be recorded
response_ends_trial | boolean | true | end trial after response
timing_stim | numeric | -1 | stimulus presentation duration. Displays indefinitely if left at default
timing_response | numeric | -1 | How long to wait for response. Wait indefinitely if left at default
prompt | string | "" | Text to display at the top of each page

## Data Generated

In addition to the [default data collected by all plugins](http://docs.jspsych.org/plugins/overview/#datacollectedbyplugins), this plugin collects the following data for each trial.


Name | Type | Value
-----|------|------
rt | numeric | response time
stimulus | string | path to or html of presented stimulus
mouse_click | string | value of button that was set up to be listened initially

## Examples

```javascript
var getHealthStim = function() {
  curr_stim = health_stims.shift()
  var stim = base_path + curr_stim
  return '<div class = dd_stimBox><img class = dd_Stim src = ' + stim + ' </img></div>' + health_response_area
}

var health_block = {
  type: 'single-stim-button',
  stimulus: getHealthStim,
  button_class: 'dd_response_button',
  data: {exp_id: 'dietary_decision', trial_id: 'health_rating'},
  timing_stim: 4000,
  timing_response: 4000,
  response_ends_trial: true,
  timing_post_trial: 500,
  on_finish: function(data) {
  	var numeric_rating = healthy_responses.indexOf(data.mouse_click)-2
    jsPsych.data.addDataToLastTrial({'stim': curr_stim.slice(0,-4), 'coded_response': numeric_rating})
    stim_ratings[curr_stim]['health'] = Number(data.mouse_click)
  }
}

```