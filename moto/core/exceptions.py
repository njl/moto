from werkzeug.exceptions import HTTPException
from jinja2 import DictLoader, Environment
from six import text_type


ERROR_RESPONSE = u"""<?xml version="1.0" encoding="UTF-8"?>
  <Response>
    <Errors>
      <Error>
        <Code>{{error_type}}</Code>
        <Message>{{message}}</Message>
        {% block extra %}{% endblock %}
      </Error>
    </Errors>
  <RequestID>7a62c49f-347e-4fc4-9331-6e8eEXAMPLE</RequestID>
</Response>
"""

ERROR_JSON_RESPONSE = u"""{
    "message": "{{message}}",
    "__type": "{{error_type}}"
}
"""

class RESTError(HTTPException):
    templates = {
        'error': ERROR_RESPONSE,
        'error_json': ERROR_JSON_RESPONSE,
    }

    def __init__(self, error_type, message, template='error', **kwargs):
        super(RESTError, self).__init__()
        env = Environment(loader=DictLoader(self.templates))
        self.error_type = error_type
        self.message = message
        self.description = env.get_template(template).render(
            error_type=error_type, message=message, **kwargs)


class JsonRESTError(RESTError):
    def __init__(self, error_type, message, template='error_json', **kwargs):
        super(JsonRESTError, self).__init__(error_type, message, template, **kwargs)

    def get_headers(self, *args, **kwargs):
        return [('Content-Type', 'application/json')]

    def get_body(self, *args, **kwargs):
        return self.description
