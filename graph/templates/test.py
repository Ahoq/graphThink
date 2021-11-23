{% extends "layout.html" %}
{% block content %}

<script type="text/javascript">

    function draw() {
        var d = $('#my-data').data();
        var config = {
            container_id: "viz",
            server_url: "bolt://localhost:7687",
            server_user: "neo4j",
            server_password: "test",
            labels: {
                'device':{
                    caption: "name",
                    size: "pageRank"
                },
                'website':{
                    caption: "name",
                    size: "pageRank"
                },
                'provider':{
                    caption: "name",
                    size: "pageRank"
                },
                'DD':{
                    caption: "name",
                    size: "pageRank"
                }
                
            },
            relationships: {
               
            },
            initial_cypher: 'p=(a:DD)-[]->() return p'
        };

        var viz = new NeoVis.default(config);
        viz.render();
    }
</script>

<script>
    window.onload = function() {
    draw();
    };
</script>
<meta id="my-data" data-name="{{device}}" data-other="{{other}}">
<div class="cont">
    <form action="{{ url_for('vis') }}" method="post">
        <select name="label_list" class="post-form">
            {% for label in labels %}
            <option name='label' value= "{{label}}" SELECTED>{{label}}</option>"
            {% endfor %}
        </select>
    </form>
    
    <!-- <select name="label_list" class="post-form">
        {% for label in labels %}
        <option name='label' value= "{{label}}" SELECTED>{{label}}</option>"
        {% endfor %}
    </select> -->
    <div id="viz"></div>
</div>
   

{% endblock %}
"MATCH p=(a:device)-[]->() RETURN p"