

/* Class to track focus shifts during experiment
*  **Requires Jquery**
*
*/
var focus_tracker = function(win) {
  var self = this;
  this.shift_away = 0;
    
  this.get_shifts = function() {
    return this.shift_away;
  };
  
  this.reset = function() {
    this.shift_away = 0;
  };
  
  $(win).blur(function() {
    self.shift_away += 1;
  });
};

var focuser = new focus_tracker(window);


/**
* **For JsPsych Only **
* Adds the experiment ID as well as the number of focus shifts and whether the experiment was in
* full screen during that trial
* @param {exp_id} string to specify the experiment id
*/
function addID(exp_id) {
  var isFullScreen = document.mozFullScreen || document.webkitIsFullScreen || (!window.screenTop && !window.screenY) 
	jsPsych.data.addDataToLastTrial({
		exp_id: exp_id,
		full_screen: isFullScreen,
		focus_shifts: focuser.get_shifts()
	})
	focuser.reset()
}

/*
* Adds a display stage rather than the generic jsPsych background element
*/
function getDisplayElement() {
  $('<div class = display_stage_background></div>').appendTo('body')
  return $('<div class = display_stage></div>').appendTo('body')
}