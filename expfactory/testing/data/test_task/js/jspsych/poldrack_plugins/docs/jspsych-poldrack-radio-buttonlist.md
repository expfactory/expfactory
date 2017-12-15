# jspsych-poldrack-radio-buttonlist plugin

Plugin to display an HTML form with radio buttons. Mostly intended for survey presentations. In many ways an earlier and more primitive version of [jspsych-survey-multi-choice.js](http://docs.jspsych.org/plugins/jspsych-multi-stim-multi-response/)

## Parameters

This table lists the parameters associated with this plugin. Parameters with a default value of *undefined* must be specified. Other parameters can be left unspecified if the default value is acceptable.

Parameter | Type | Default Value | Description
----------|------|---------------|------------
preamble | string | "" | Text to present at the top of each page
buttonlist | string | "" | HTML table embedded in the form. Multiple pages can be added by embedding this in a timeline
checkAll | boolean | false | Are all questions on the page mandatory
numq | numeric | 0 | How many questions there are on the page

## Data Generated

In addition to the [default data collected by all plugins](http://docs.jspsych.org/plugins/overview/#datacollectedbyplugins), this plugin collects the following data for each trial.


Name | Type | Value
-----|------|------
response | numeric or string | Values of the buttons that are coded in the buttonlist html


## Examples

#### Example survey with two pages

```javascript
// defining groups of questions that will go together.
var page_1_questions = ["Admitting that your tastes are different from those of a friend.", "Going camping in the wilderness.", "Betting a day's income at the horse races.", "Investing 10% of your annual income in a moderate growth diversified fund.", "Drinking heavily at a social function.", "Taking some questionable deductions on your income tax return."];
var page_2_questions = ["Disagreeing with an authority figure on a major issue.", "Betting a day's income at a high-stake poker game.", "Having an affair with a married man/woman.", "Passing off somebody else’s work as your own.", "Going down a ski run that is beyond your ability.", "Investing 5% of your annual income in a very speculative stock."];

// definiting response scale.
var scale = ["Extremely Unlikely", "Moderately Unlikely", "Somewhat Unlikely", "Not Sure", "Somewhat Likely", "Moderately Likely", "Extremely Likely"];

//defining preamble text for each page.
// var pretext =['<p><strong>Please indicate the likelihood that you would engage in the described activity or behavior if you were to find yourself in that situation.</strong></p>']

var pretext ='<p><strong>Please indicate the likelihood that you would engage in the described activity or behavior if you were to find yourself in that situation.</strong></p>'


var header = []

for (var i = 0; i < scale.length; i++){
  header += '<th>'+scale[i]+'</th>'
}

var page_1_buttonlist = ['<table><tr><th></th>']

page_1_buttonlist += header + '</tr>'

for (var i = 0; i < page_1_questions.length; i++){
  page_1_buttonlist += '<tr><td>'+ page_1_questions[i] +'</td><td><center><input type="radio" name="response_' + i + '" value = "1"></center></td><td><center><input type="radio" name="response_' + i + '" value = "2"></center></td><td><center><input type="radio" name="response_' + i + '" value = "3"></center></td><td><center><input type="radio" name="response_' + i + '" value = "4"></center></td><td><center><input type="radio" name="response_' + i + '" value = "5"></center></td><td><center><input type="radio" name="response_' + i + '" value = "6"></center></td><td><center><input type="radio" name="response_' + i + '" value = "7"></center></td></tr>'
}

page_1_buttonlist += '</table>'

var page_2_buttonlist = ['<table><tr><th></th>']

page_2_buttonlist += header + '</tr>'

for (var i = 0; i < page_2_questions.length; i++){
  page_2_buttonlist += '<tr><td>'+ page_2_questions[i] +'</td><td><center><input type="radio" name="response_' + i + '" value = "1"></center></td><td><center><input type="radio" name="response_' + i + '" value = "2"></center></td><td><center><input type="radio" name="response_' + i + '" value = "3"></center></td><td><center><input type="radio" name="response_' + i + '" value = "4"></center></td><td><center><input type="radio" name="response_' + i + '" value = "5"></center></td><td><center><input type="radio" name="response_' + i + '" value = "6"></center></td><td><center><input type="radio" name="response_' + i + '" value = "7"></center></td></tr>'
}

page_2_buttonlist += '</table>'

var survey_block = {
    type: 'radio-buttonlist',
    timeline: [{buttonlist: page_1_buttonlist},{buttonlist: page_2_buttonlist}],
    preamble: pretext,
    checkAll: true,
    numq: 6
};
```