import re

from xmlrpclib import ServerProxy

API_URL = 'https://{user}:{password}@samurai.sipgate.net/RPC2'

CLIENT_NAME = 'pysipgate'
CLIENT_VENDOR = 'http://chaossource.net/'

def sanitize_number(number):
    return re.sub('[\s\-]', '', number)

class SipgateConnection:

    def __init__(self, user, password):
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
        self.default_ep.call(number)

    def voice_endpoints(self):
        return tos_endpoints('voice')

    def fax_endpoints(self):
        return tos_endpoints('fax')

    def tos_endpoints(self, tos):
        return filter(lambda ep: tos in ep.tos, self.endpoints)

    def balance(self):
        balance = self.server.samurai.BalanceGet()['CurrentBalance']
        return (balance['TotalIncludingVat'], balance['Currency'])

    def greeting(self):
        res = self.server.samurai.UserdataGreetingGet()
        del res['StatusCode']
        del res['StatusString']
        return res

class SipgateEndpoint:

    def __init__(self, con, data):
        self.con = con

        self.uri = data['SipUri']
        self.tos = data['TOS']
        self.alias = data.get('UriAlias', None)

    def name(self):
        if self.alias:
            return self.alias
        else:
            match = re.match('sip:(.*)@sipgate\.de', self.uri)

            if match:
                return match.group(1)
            else:
                return self.uri

    def voice(self, number):
        remote_uri = 'sip:{}@sipgate.de'.format(sanitize_number(number))

        data = {
                'LocalUri': self.uri,
                'RemoteUri': remote_uri,
                'TOS': 'voice',
                }

        res = self.con.server.samurai.SessionInitiate(data)

        return SipgateSession(self.con, res['SessionID'])

class SipgateSession:

    def __init__(self, con, sid):
        self.con = con
        self.sid = sid

    def state(self):
        res = self.con.server.samurai.SessionStatusGet({'SessionID': self.sid})
        return res['SessionStatus']

    def close(self):
        self.con.server.samurai.SessionClose({'SessionID': self.sid})

