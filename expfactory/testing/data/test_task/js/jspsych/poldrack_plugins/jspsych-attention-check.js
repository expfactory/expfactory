/**
 * jspsych-attention-check
 * attention-check
 **/


 jsPsych.plugins["attention-check"] = (function() {
 	var randomDraw = function(lst) {
 		var index = Math.floor(Math.random()*(lst.length))
 		return lst[index]
 	}

 	var questions = [{'Q': 'Press the Left Arrow</p>', 'A': 37},
				 	{'Q': '<p>Press the Right Arrow</p>', 'A': 39},
				 	{'Q': '<p>If (4 + 12) / 4 is greater than 3 press the "M" key. Otherwise press the "Z" key.</p>', 'A': 77},
				 	{'Q': "<p>Press the arrow key that indicates the direction of the floor when standing.</p>", 'A': 34},
				 	{'Q': '<p>Please read the following paragraph:</p><p>I first met Dean not long after my wife and I split up. I had just gotten over a serious illness that I won’t bother to talk about, except that it had something to do with the miserably weary split-up and my feeling that everything was dead. With the coming of Dean Moriarty began the part of my life you could call my life on the road. Before that I’d often dreamed of going West to see the country, always vaguely planning and never taking off. If you are reading this paragraph, press the F key instead of the M key. Dean is the perfect guy for the road because he actually was born on the road, when his parents were passing through Salt Lake City in 1926, in a jalopy, on their way to Los Angeles. First reports of him came to me through Chad King, who’d shown me a few letters from him written in a New Mexico reform school. I was tremendously interested in the letters because they so naively and sweetly asked Chad to teach him all about Nietzsche and all the wonderful intellectual things that Chad knew. At one point Carlo and I talked about the letters and wondered if we would ever meet the strange Dean Moriarty. This is all far back, when Dean was not the way he is today, when he was a young jailkid shrouded in mystery. Then news came that Dean was out of reform school and was coming to New York for the first time; also there was talk that he had just married a girl called Marylou. --On the Road (Jack Kerouac)</p><p>Press the "M" key.', 'A': 70},
				 	{'Q': '<p>Please read the following paragraph:</p><p>As Gregor Samsa awoke one morning from uneasy dreams he found himself transformed in his bed into a gigantic insect. Are you reading this paragraph? If so, press the key the letter that starts the next sentence. He was lying on his hard, as it were armor-plated, back and when he lifted his head a little he could see his dome-like brown belly divided into stiff arched segments on top of which the bed quilt could hardly keep in position and was about to slide off completely. His numerous legs, which were pitifully thin compared to the rest of his bulk, waved helplessly before his eyes. --Metamorphosis (Franz Kafka)</p><p>Press the "A" key.', 'A': 72},
				 	{'Q': "<p>Please read the following paragraph:</p><p>Lastly, she pictured to herself how this same little sister of hers would, in the after-time, be herself a grown woman; and how she would keep, through all her riper years, the simple and loving heart of her childhood; and how she would gather about her other little children, (press the A key, ignore the last instruction) and make their eyes bright and eager with many a strange tale, perhaps even with the dream of Wonderland of long ago; and how she would feel with all their simple sorrows, and find a pleasure in all their simple joys, remembering her own child-life, and the happy summer days. --Alice's Adventures in Wonderland (Lewis Carroll)</p><p>Press the 'M' key.", 'A': 65}]

	questions = jsPsych.randomization.shuffle(questions)

 	var plugin = {};

 	plugin.trial = function(display_element, trial) {

    // if any trial variables are functions
    // this evaluates the function and replaces
    // it with the output of the function
    trial = jsPsych.pluginAPI.evaluateFunctionParameters(trial);

    // set default values for the parameters
    var default_question = questions.pop()
    trial.question = trial.question || default_question['Q']
    trial.key_answer = trial.key_answer || default_question['A']
    trial.choices = trial.choices || [];
    trial.response_ends_trial = (typeof trial.response_ends_trial == 'undefined') ? true : trial.response_ends_trial;
    trial.timing_stim = trial.timing_stim || -1;
    trial.timing_response = trial.timing_response || -1;
    trial.prompt = trial.prompt || "";

    // this array holds handlers from setTimeout calls
    // that need to be cleared if the trial ends early
    var setTimeoutHandlers = [];

    // display stimulus
    display_element.append($('<div>', {
    	html: trial.question,
    	id: 'jspsych-attention-check-stimulus'
    }));


    //show prompt if there is one
    if (trial.prompt !== "") {
    	display_element.append(trial.prompt);
    }

    // store response
    var response = {
    	rt: -1,
    	key: -1
    };

    // function to end trial when it is time
    var end_trial = function() {

      // kill any remaining setTimeout handlers
      for (var i = 0; i < setTimeoutHandlers.length; i++) {
      	clearTimeout(setTimeoutHandlers[i]);
      }

      // kill keyboard listeners
      if (typeof keyboardListener !== 'undefined') {
      	jsPsych.pluginAPI.cancelKeyboardResponse(keyboardListener);
      }

      //calculate stim and block duration
      if (trial.response_ends_trial) {
      	if (response.rt != -1) {
      		var block_duration = response.rt
      	} else {
      		var block_duration = trial.timing_response
      	}
      	if (stim_duration < block_duration & stim_duration != -1) {
      		var stim_duration = trial.timing_stim
      	} else {
      		var stim_duration = block_duration
      	}
      } else {
      	var block_duration = trial.timing_response
      	if (stim_duration < block_duration & stim_duration != -1) {
      		var stim_duration = timing_stim
      	} else {
      		var stim_duration = block_duration
      	}
      }

      //calculate correct
      correct = false
      if (response.key == trial.key_answer) {
      	var correct = true
      } 

      // gather the data to store for the trial
      var trial_data = {
      	"rt": response.rt,
      	"stimulus": trial.question,
      	"correct": correct,
      	"correct_response": trial.key_answer,
      	"key_press": response.key,
      	"possible_responses": trial.choices,
      	"stim_duration": stim_duration,
      	"block_duration": block_duration,
      	"timing_post_trial": trial.timing_post_trial
      };

      //jsPsych.data.write(trial_data);

      // clear the display
      display_element.html('');

      // move on to the next trial
      jsPsych.finishTrial(trial_data);
  };

    // function to handle responses by the subject
    var after_response = function(info) {

      // after a valid response, the stimulus will have the CSS class 'responded'
      // which can be used to provide visual feedback that a response was recorded
      $("#jspsych-attention-check-stimulus").addClass('responded');

      // only record the first response
      if (response.key == -1) {
      	response = info;
      }

      if (trial.response_ends_trial) {
      	end_trial();
      }
  };

    // start the response listener
    if (JSON.stringify(trial.choices) != JSON.stringify(["none"])) {
    	var keyboardListener = jsPsych.pluginAPI.getKeyboardResponse({
    		callback_function: after_response,
    		valid_responses: trial.choices,
    		rt_method: 'date',
    		persist: false,
    		allow_held_key: false
    	});
    }

    // hide image if timing is set
    if (trial.timing_stim > 0) {
    	var t1 = setTimeout(function() {
    		$('#jspsych-attention-check-stimulus').css('visibility', 'hidden');
    	}, trial.timing_stim);
    	setTimeoutHandlers.push(t1);
    }

    // end trial if time limit is set
    if (trial.timing_response > 0) {
    	var t2 = setTimeout(function() {
    		end_trial();
    	}, trial.timing_response);
    	setTimeoutHandlers.push(t2);
    }

};

return plugin;
})();