---
layout: null
title: The Experiment Factory
permalink: /pdf
---

<div id="content">
    {% for page in site.pages %}
         {% if page.pdf %}
             {{ page.content | markdownify }}
         {% endif %}
    {% endfor %}
</div>

<script src="https://code.jquery.com/jquery-1.12.3.min.js"></script>
<script src="https://cdnjs.cloudflare.com/ajax/libs/jspdf/0.9.0rc1/jspdf.min.js"></script>

<script>
$("button").remove()
</script>
