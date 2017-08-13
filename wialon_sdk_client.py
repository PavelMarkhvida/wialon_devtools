import grequests
import requests
from PyQt5 import QtCore, QtNetwork
import json
import time


class WialonSDKClient():

	def __init__(self):
		self.protocol = 'http'
		self.ip = '10.0.2.15'
		self.port = '8021'
		self.login = 'wialon'
		self.password = 'password'
		self.sid = None
		self.nm = QtNetwork.QNetworkAccessManager()


	def do_login(self, cb):
		"Try to login/relogin"

		if not self.ip:
			cb(1, 'Host isn\'t specified')
			return

		if not self.port:
			cb(1, 'Port isn\'t specified')
			return

		if not self.login:
			cb(1, 'Please, provide username')
			return

		login_url = '{}://{}:{}/oauth/authorize.html'.format(self.protocol, self.ip, self.port)

		data = {
			'client_id': 'Devtools',
			'login': self.login,
			'passw': self.password,
			'response_type': 'token',
			'activation_time': 0,
			'duration': 22592000,
			'redirect_uri': 'devtools://redir',
			'access_type': 0x100
		}

		self.post(login_url, data, self.finish_login, cb)


	def finish_login(self, reply, cb):
		if reply.error() != QtNetwork.QNetworkReply.NoError:
			cb(1, 'Auth failed')
			return

		access_token = None
		if reply.hasRawHeader(b'Location'):
			access_token = get_token(reply.header(QtNetwork.QNetworkRequest.LocationHeader).toString())
		else:
			cb(1, 'Auth failed')
			return

		token_url = '{}://{}:{}/wialon/ajax.html'.format(self.protocol, self.ip, self.port)

		data = {
			'svc': 'token/login',
			'params': json.dumps({'token': access_token})
		}

		self.post(token_url, data, self.finish_get_sid, cb)


	def finish_get_sid(self, reply, cb):
		if reply.error() != QtNetwork.QNetworkReply.NoError:
			cb(1, 'Auth failed')
			return

		response = json.loads(reply.readAll().data().decode('ascii'))

		self.sid = response['eid']
		cb(0, 'Auth successfull')
		

	def execute_request(self, svc, params):
		if not svc:
			return 'Service isn\'t specified'

		if not self.ip:
			return 'Host isn\'t specified'

		if not self.port:
			return 'Port isn\'t specified'

		if not sid_valid():
			login_result = self.do_login()
			if not login_result[0]:
				return login_result[1]

		data = {
			'sid': self.sid,
			'svc': svc,
			'params': params
		}

		r = requests.post('https://%s:%d/wialon/ajax.html'.format(self.ip, self.port), params=data)
		return r.text


	def set_ip(self, ip):
		self.ip = ip


	def get_ip(self):
		return self.ip


	def set_port(self, port):
		self.port = port


	def get_port(self):
		return self.port


	def is_secure(self):
		return self.protocol is 'https'


	def set_secure(self, secure):
		if secure:
			self.protocol = 'https'
			self.port = '443'
		else:
			self.protocol = 'http'
			if self.port == '443':
				self.port = '8021'


	def set_sid(self, sid):
		self.sid = sid


	def get_sid(self):
		return self.sid


	def sid_valid(self):
		return self.sid # and len(self.sid) is 32


	def set_login(self, login):
		self.login = login


	def get_login(self):
		return self.login


	def set_password(self, password):
		self.password = password


	def get_password(self):
		return self.password

	def post(self, url, data, cb, cb_args):
		body = QtCore.QByteArray()
		body.append('&'.join(k + '=' + str(v) for k,v in data.items()))

		qurl = QtCore.QUrl(url)
		request = QtNetwork.QNetworkRequest(qurl)
		request.setHeader(QtNetwork.QNetworkRequest.ContentTypeHeader, "application/x-www-form-urlencoded")
		reply = self.nm.post(request, body)
		reply.ignoreSslErrors()
		reply.finished.connect(callback_factory(reply=reply, cb=cb, cb_args=cb_args))


def callback_factory(*factory_args, **factory_kwargs):
	def response_hook(*args, **kwargs):
		factory_kwargs['cb'](factory_kwargs['reply'], factory_kwargs['cb_args'])
	return response_hook


def get_token(url):
	query = url.split('?')[1]
	params = query.split('&')
	for p in params:
		if 'access_token' in p:
			return p.split('=')[1]