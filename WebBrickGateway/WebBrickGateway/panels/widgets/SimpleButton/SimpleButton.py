# $Id: SimpleButton.py 2696 2008-09-05 09:33:43Z graham.klyne $
#
# Widget class for simple button on a form
#

from urlparse import urljoin

from turbogears.widgets.base  import Widget, CompoundWidget, WidgetsList
from turbogears.widgets.forms import FormField, Button
from EventLib.URI             import EventBaseUri, EventSourceBase

SetButtonTextEvent  = urljoin(EventBaseUri, "SetButtonText")
SetButtonStateEvent = urljoin(EventBaseUri, "SetButtonState")
ButtonClickEvent    = urljoin(EventBaseUri, "ButtonClickEvent")

class SimpleButton(FormField):
    template = """
    <input xmlns:py="http://purl.org/kid/ns#"
        type="button"
        InitializeWidget="SimpleButton_Init"
        class="button_normal"
        value="${value}"
        py:attrs="attrs"
    >
    </input>
    """
    params = ["attrs", "id"]
    params_doc = {'attrs' : 'Dictionary containing extra (X)HTML attributes for'
                            ' the button input tag'}
    attrs = {}

    def update_params(self, d):
        super(SimpleButton, self).update_params(d)
        d['attrs']['SetButtonTextEvent']  = SetButtonTextEvent
        d['attrs']['SetButtonStateEvent'] = SetButtonStateEvent
        d['attrs']['ButtonClickEvent']    = ButtonClickEvent
        d['attrs']['ButtonClickSource']   = urljoin(EventBaseUri, d["value"])
        if self.is_named:
            d['attrs']['name'] = d["name"]
            d['attrs']['ButtonClickSource'] = urljoin(EventBaseUri, d["name"])
        if d.has_key("id"):
            d['attrs']['id']   = d["id"]
            d['attrs']['ButtonClickSource'] = urljoin(EventBaseUri, d["id"])

# End.
