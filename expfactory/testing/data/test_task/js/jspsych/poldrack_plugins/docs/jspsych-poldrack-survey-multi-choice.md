# jspsych-poldrack-survey-multi-choice

Modified version of the original [jspsych-survey-multi-choice](http://docs.jspsych.org/plugins/jspsych-survey-multi-choice/) plugin. Very similar to the jspsych-poldrack-radio-buttonlist plugin but has more built-in HTML features (and less flexibility). Features added to the original plugin include: 

* Storing each question's data in separate rows 
* Both the text and numeric codes for the response option 
* Scored numeric data
* Progress bars
* Response range in output 
* Include question data in output
* Back buttons

## Parameters

This table lists the parameters associated with this plugin. Parameters with a default value of *undefined* must be specified. Other parameters can be left unspecified if the default value is acceptable.

Parameter | Type | Default Value | Description
----------|------|---------------|------------
exp_id | string | "" | Name of survey that will be included in output for `exp_id`
preamble | string | "" | Text to show above each page.
required | array  | null | Should have same dimensions as pages. Values should be booleans indicating whether question is mandatory.
horizontal | boolean | false | Should response options be displayed horizontally on a single line.
pages | array | "" | Array of arrays containing questions. Should include an array for each page that contains the questions to be displayed on each page.
show_clickable_nav | boolean | true | Whether to display navigation buttons.
allow_backward | boolean | true | Whether to allow a back button to navigate to previous pages.
options | array | NA | Array with an array for each page that contains array with responses for each question (i.e. 3 dim array instead of 2 options\[current_page\]\[current_question\]\[current_option\])
scale | array of objects | NA | Array containing objects containing how any option should be coded numerically
input | array of arrays | radio | option to specify different types of input (current options: `"radio"`, `"text"`, `"checkbox"`, `"number"`)

## Data Generated

In addition to the [default data collected by all plugins](http://docs.jspsych.org/plugins/overview/#datacollectedbyplugins), this plugin collects the following data for each trial.


Name | Type | Value
-----|------|------
rt | numeric | total number of ms spent on that page
qnum | numeric | question number on a given page
page_num | numeric | page number question was presented in
trial_num | numeric | continous trial number variable
stim_question | text | text of question that participant saw
stim_response | text | text of response option participant selected
score_response | numeric | numeric value of scored response as specified in `scale` parameter
response_range | numeric | range of available responses
times_viewed | numeric | number of times page was viewed
view_history | js object | the last row of output containing raw js data on order of page views

## Examples

```javascript
function fillArray(value, len) {
  if (len == 0) return [];
  var a = [value];
  while (a.length * 2 <= len) a = a.concat(a);
  if (a.length < len) a = a.concat(a.slice(0, len - a.length));
  return a;
}

var opts = ["Disagree strongly", "Disagree moderately", "Disagree a little",
  "Neither agree nor disagree", "Agree a little", "Agree moderately", "Agree strongly"
]
var scale_reg = {
  "Disagree strongly": 1,
  "Disagree moderately": 2,
  "Disagree a little": 3,
  "Neither agree nor disagree": 4,
  "Agree a little": 5,
  "Agree moderately": 6,
  "Agree strongly": 7
}
var scale_rev = {
  "Disagree strongly": 7,
  "Disagree moderately": 6,
  "Disagree a little": 5,
  "Neither agree nor disagree": 4,
  "Agree a little": 3,
  "Agree moderately": 2,
  "Agree strongly": 1
}

var all_pages = [
  ["Extraverted, enthusiastic.", "Critical, quarrelsome.", "Dependable, self-disciplined.",
    "Anxious, easily upset.", "Open to new experiences, complex.", "Reserved, quiet.",
    "Sympathetic, warm.", "Disorganized, careless.", "Calm, emotionally stable.",
    "Conventional, uncreative."
  ]
]

var all_options = [fillArray(opts, 10)]

var score_scale = [
    [scale_reg, scale_rev, scale_reg, scale_rev, scale_reg, scale_rev, scale_reg, scale_rev, scale_reg, scale_rev]
  ]

var survey_block = {
  type: "poldrack-survey-multi-choice",
  exp_id: "ten_item_personality",
  horizontal: true,
  preamble: '<p><strong>I see myself as:</strong></p>',
  pages: all_pages,
  options: all_options,
  scale: score_scale,
  show_clickable_nav: true,
  allow_backward: true,
  required: [fillArray(true, 10)]
};
```