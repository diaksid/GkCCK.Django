{% load i18n %}


<form
    id="{{ form.prefix }}-form"
    {% if class %}class="{{ class }}"{% endif %}
    action="{% url 'postbox:send' %}"
    method="post"
>
    {% csrf_token %}

    <input
        name="prefix"
        type="hidden"
        value="{{ form.prefix }}"
     >

    {% for field in form %}
        <div class="form-group{% if field.errors %} has-error{% endif %}">
            <label
                class="sr-only"
                for="{{ field.id_for_label }}"
            >{% trans field.label %}</label>

            {{ field|safe }}

            {% if field.errors %}
                <span class="help-block">{{ field.errors }}</span>
            {% endif %}
        </div>
    {% endfor %}

    <div class="form-group pull-last">
        <button
            class="btn btn-lg btn-primary"
            type="submit"
        ><span class="icon icon-send"></span></button>
    </div>
</form>
