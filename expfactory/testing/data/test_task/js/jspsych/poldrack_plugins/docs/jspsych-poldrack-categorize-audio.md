# jspsych-poldrack-categorize-audio plugin

Plugin for playing an audio file, getting a keyboard response, and giving feedback.

## Parameters

This table lists the parameters associated with this plugin. Parameters with a default value of *undefined* must be specified. Other parameters can be left unspecified if the default value is acceptable.

Parameter | Type | Default Value | Description
----------|------|---------------|------------
stimuli | string | NA | Path to audio file
choices | array | [] | Accepted responses
key_answer | boolean | NA | option to show image for fixed time interval, ignoring key responses, true = image will keep displaying after response, false = trial will immediately advance when response is recorded
text_answer | string | "" | String that replaces correct or incorrect text
correct_text | string | "" | Text for feedback on correct trials
incorrect_text | string | "" | Text for feedback on incorrect trials
response_ends_trial | boolean | true | Advance to next trial following response
force_correct_button_press | boolean | false | Accept only specified button as response
prompt | string | "" | Text to display on top at each trial
show_feedback_on_timeout | boolean | false | Option to specify whether feedback should be given when trial timeouts
timeout_message | string | "Please respond faster." | What message would be shown if `show_feedback_on_timeout` is true
timing_response | numeric | -1 | how long to wait for response, if -1 then wait for response forever
timing_feedback_duration | numeric | 2000 | how long after trial feedback is displayed


## Data Generated

In addition to the [default data collected by all plugins](http://docs.jspsych.org/plugins/overview/#datacollectedbyplugins), this plugin collects the following data for each trial.


Name | Type | Value
-----|------|------

rt | numeric | response time
correct | boolean | whether response was correct
stimulus | string | path to audio file
key_press | numeric | response key

## Examples

```javascript
practice_stims = [{sound: 'static/experiments/tone_monitoring/sounds/880Hz_-6dBFS_.5s.mp3',
		  data: {exp_id: 'tone_monitoring', trial_id: 'high', condition: 'practice'}},
		 {sound: 'static/experiments/tone_monitoring/sounds/440Hz_-6dBFS_.5s.mp3',
		  data: {exp_id: 'tone_monitoring', trial_id: 'medium', condition: 'practice'}},
		 {sound: 'static/experiments/tone_monitoring/sounds/220Hz_-6dBFS_.5s.mp3',
		 data: {exp_id: 'tone_monitoring', trial_id: 'low', condition: 'practice'}}
]

last_tone = randomDraw(practice_stims)
practice_trials = jsPsych.randomization.repeat(practice_stims,8, true);
practice_trials.sound.push(last_tone.sound)
practice_trials.data.push(last_tone.data)

for (i = 0; i< practice_trials.sound.length; i++) {	
	var practice_tone_block = {
	  type: 'categorize-audio',
	  stimuli: [practice_trials.sound[i]],
	  data: [practice_trials.data[i]],
	  key_answer: get_correct_key,
	  correct_text: '<div class = centerbox><div class = center-text>Correct</div></div>',
	  incorrect_text: '<div class = centerbox><div class = center-text>Incorrect</div></div>',
	  timeout_message: ' ',
	  choices: [32],
	  timing_response: 2000,
	  timing_feedback_duration: 1000,
	  timing_post_trial: 500,
	  on_trial_start: update_count,
	  on_finish: reset_count,
	  prompt: '<div class = centerbox><div class = block-text>Press the spacebar when any tone repeats four times. After you press the spacebar (for any reason), reset your count for that tone.</div></div>'
	};
	tone_monitoring_experiment.push(update_function)
	tone_monitoring_experiment.push(practice_tone_block)
}
```