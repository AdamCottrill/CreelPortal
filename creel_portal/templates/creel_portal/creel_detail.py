{% extends "base.html" %}



{% block content %}

<ul>
<li>{{ object.year }}</li>
<li>{{ object.prj_cd }}</li>
<li>{{ object.prj_nm }}</li>
<li>{{ object.prj_date0 }}</li>
<li>{{ object.prj_date1 }}</li>
</ul>

{% endblock content %}
