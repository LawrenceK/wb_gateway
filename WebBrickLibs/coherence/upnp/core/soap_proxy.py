# Licensed under the MIT license
# http://opensource.org/licenses/mit-license.php

# Copyright 2007 - Frank Scholz <coherence@beebits.net>

from coherence import log

from coherence.extern.et import ET, namespace_map_update

from coherence.upnp.core.utils import getPage, parse_xml

from coherence.upnp.core import soap_lite

class SOAPProxy(log.Loggable):
    """ A Proxy for making remote SOAP calls.

        Based upon twisted.web.soap.Proxy and
        extracted to remove the SOAPpy dependency

        Pass the URL of the remote SOAP server to the constructor.

        Use proxy.callRemote('foobar', 1, 2) to call remote method
        'foobar' with args 1 and 2, proxy.callRemote('foobar', x=1)
        will call foobar with named argument 'x'.
    """

    logCategory = 'soap'

    def __init__(self, url, namespace=None, envelope_attrib=None, header=None, soapaction=None):
        self.url = url
        self.namespace = namespace
        self.header = header
        self.action = None
        self.soapaction = soapaction
        self.envelope_attrib = envelope_attrib

    def log_dom(self,dom):
        for c in dom.getchildren():
            self.debug("%s) %s = %s", c, c.tag, c.text)
            self.log_dom(c)

    def callRemote(self, soapmethod, *args, **kwargs):
        soapaction = soapmethod or self.soapaction
        if '#' not in soapaction:
            soapaction = '#'.join((self.namespace[1],soapaction))
        self.action = soapaction.split('#')[1]

        self.info("callRemote %r %r %r %r", self.soapaction, soapmethod, self.namespace, self.action)

        headers = { 'content-type': 'text/xml ;charset="utf-8"',
                    'SOAPACTION': '"%s"' % soapaction,}
        if kwargs.has_key('headers'):
            headers.update(kwargs['headers'])
            del kwargs['headers']

        payload = soap_lite.build_soap_call("{%s}%s" % (self.namespace[1], self.action), kwargs,
                                            encoding=None)

        self.info("callRemote soapaction %s %s: ", self.action, self.url)
        self.debug("callRemote payload: %s", payload)

        def gotError(failure, url):
            # failure.value should be an Error object
            self.error("error requesting %s %s %s [%s]", url, failure, failure.value.status, failure.value.response )

            if int(failure.value.status) == 500:
                # generic error, do we have abody?
                # if so parse and return.
                tree = parse_xml(failure.value.response)
                self.log_dom(tree.getroot())

            return failure

        return getPage(self.url, postdata=payload, method="POST",
                        headers=headers
                      ).addCallbacks(self._cbGotResult, gotError, None, None, [self.url], None)

    def _cbGotResult(self, result):
        page, headers = result
        self.debug( "_cbGotResult %s [%s]", headers, page )

        tree = parse_xml(page)
        self.log_dom(tree.getroot())

        body = tree.find('{http://schemas.xmlsoap.org/soap/envelope/}Body')
        #print "body", body
        response = body.find('{%s}%sResponse' % (self.namespace[1], self.action))
        if response == None:
            """ fallback for improper SOAP action responses """
            response = body.find('%sResponse' % self.action)
        self.debug("callRemote response %s", response)
        result = {}
        if response != None:
            for elem in response:
                result[elem.tag] = self.decode_result(elem)
        self.debug( "result %s", result )

        return result

    def decode_result(self, element):
        type = element.get('{http://www.w3.org/1999/XMLSchema-instance}type')
        if type is not None:
            try:
                prefix, local = type.split(":")
                if prefix == 'xsd':
                    type = local
            except ValueError:
                pass

        if type == "integer" or type == "int":
            return int(element.text)
        if type == "float" or type == "double":
            return float(element.text)
        if type == "boolean":
            return element.text == "true"

        return element.text or ""
