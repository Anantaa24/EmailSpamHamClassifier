var tabledata ={
{% if allemail|length == 0 %}
      <div class="alert alert-dark" role="alert">
  No record found!
</div>
    {% else %}
{% for mail in allemail %}
{{loop.index}},
{{mail.email}},
{{mail.date_created}},
{{mail.category}},
{% endfor %}
}

var state ={
'querySet':tabledata,

'page':1,
'rows':5
}

function pagination(querySet, page, rows){
var trimstart = (page-1)*rows
var trimend = trimstart *rows
}