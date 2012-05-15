import re

from xmlrpclib import ServerProxy, ProtocolError, Error, Fault

API_URL = 'https://{user}:{password}@samurai.sipgate.net/RPC2'

CLIENT_NAME = 'pysipgate'
CLIENT_VENDOR = 'https://github.com/thammi/pysipgate'

class SipgateException(Exception):
    pass

class SipgateAuthException(SipgateException):
    pass

def exception_converter(fun):
    def decorated(*args, **kargs):
        # xmlrpclib has different kinds of excptions which are incompatible ...
        try:
            fun(*args, **kargs)
        except ProtocolError as e:
            if e.errcode == 401:
                raise SipgateAuthException(e.errmsg)
            else:
                raise SipgateException(e.errmsg)
        except Fault as e:
            raise SipgateException(e.faultString)

    return decorated


def sanitize_number(number):
    """Tries to sanitize a phone number for usabe by the Sipgate API"""
    return re.sub('\D', '', number)

class SipgateConnection:
    """Represents a connection to the Sipgate API Server"""

    @exception_converter
    def __init__(self, user, password):
        """Create a connection object for the given username"""
        url = API_URL.format(user=user, password=password)

        self.server = server = ServerProxy(url)
        server.samurai.ClientIdentify({'ClientName': CLIENT_NAME, 'ClientVendor': CLIENT_VENDOR})

        self.endpoints = endpoints = []
        self.default_ep = None

        res = server.samurai.OwnUriListGet()

        for ep_data in res['OwnUriList']:
            ep = SipgateEndpoint(self, ep_data)

            endpoints.append(ep)

            if ep_data['DefaultUri']:
                self.default_ep = ep

    def voice(self, number):
        """Initiate a voice call with the given number.

        The default endpoint is used to initiate the voice call.

        """
        self.default_ep.call(number)

    def voice_endpoints(self):
        """Returns all endpoints which can handle voice calls"""
        return self.tos_endpoints('voice')

    def fax_endpoints(self):
        """Returns all endpoints which can handle fax messages"""
        return self.tos_endpoints('fax')

    def tos_endpoints(self, tos):
        """Returns all endpoints which support the given type of service"""
        return filter(lambda ep: tos in ep.tos, self.endpoints)

    @exception_converter
    def balance(self):
        """Returns the balance of the account

        The result is a tuple consisting of the balance and the currency it is
        represented in.

        """
        balance = self.server.samurai.BalanceGet()['CurrentBalance']
        return (balance['TotalIncludingVat'], balance['Currency'])

    @exception_converter
    def greeting(self):
        """Returns an object containing the greeting used for this account"""
        res = self.server.samurai.UserdataGreetingGet()
        del res['StatusCode']
        del res['StatusString']
        return res

class SipgateEndpoint:
    """Represents an endpoint in the Sipgate API.

    Endpoints can serve different types of service and multiple devices can be
    connected to an endpoint.

    """

    def __init__(self, con, data):
        """Creates an endpoint object for a connection"""

        self.con = con

        self.uri = data['SipUri']
        self.tos = data['TOS']
        self.alias = data.get('UriAlias', None)
        self.default = data['DefaultUri']

    def name(self):
        """Returns a name which is as humanly readable as possible"""

        if self.alias:
            return self.alias
        else:
            match = re.match('sip:(.*)@sipgate\.de', self.uri)

            if match:
                return match.group(1)
            else:
                return self.uri

    @exception_converter
    def voice(self, number):
        """Initiate a voice call with the given number."""

        remote_uri = 'sip:{}@sipgate.de'.format(sanitize_number(number))

        data = {
                'LocalUri': self.uri,
                'RemoteUri': remote_uri,
                'TOS': 'voice',
                }

        res = self.con.server.samurai.SessionInitiate(data)

        return SipgateSession(self.con, res['SessionID'])

class SipgateSession:
    """Represents a session between a local and a remote endpoint"""

    def __init__(self, con, sid):
        """Creates a sesseion object representing a Sipgate session"""

        self.con = con
        self.sid = sid

    @exception_converter
    def state(self):
        """Returns the human readable state of the session"""

        res = self.con.server.samurai.SessionStatusGet({'SessionID': self.sid})
        return res['SessionStatus']

    @exception_converter
    def close(self):
        """Closes the session"""

        self.con.server.samurai.SessionClose({'SessionID': self.sid})

