# jspsych-consent plugin

This plugin display text intended for a consent form that is displayed with a checkbox at the bottom for participants to indicate they are willing to participate in the experiment. The page does not advance until the checkbox is selected. The text for presentation is HTML content so it can be versatile .

## Parameters

This table lists the parameters associated with this plugin. Parameters with a default value of *undefined* must be specified. Other parameters can be left unspecified if the default value is acceptable.


Parameter | Type | Default Value | Description
----------|------|---------------|------------
consent_text | string | "" | Text that should be acknowledged to continue with the experiment
checkbox_text | string | "Check here" | Text for the checkbox
button_text | string | "Continue" | Text for the button to advance pages
container | string | -1 | Not used right now but later can include formating for the container the consent_text appears in. Right now, this should be specified in the HTML string for consent_text

## Data Generated

In addition to the [default data collected by all plugins](http://docs.jspsych.org/plugins/overview/#datacollectedbyplugins), this plugin collects the following data for each trial.

Name | Type | Value
-----|------|------
rt | numeric | The response time in milliseconds for the subject to make a response. The time is measured from when the stimulus first appears on the screen until the subject's response.

## Examples

#### Displaying consent text

```javascript
var consent_block = {
          type:'consent',
          consent_text:'<div class = centerbox><p class = block-text>Welcome to the experiment. Please sign away your brain.</p><br></br>',
          checkbox_text: 'I agree to participate in this study.',
          button_text: "Begin experiment!",
          timing_post_trial: 0
        };
```