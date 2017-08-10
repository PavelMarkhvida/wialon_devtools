import grequests
import requests
import json
import time

def callback_factory(*factory_args, **factory_kwargs):
	def response_hook(response, *args, **kwargs):
		print('response received' + str(response))
		time.sleep(5)
		factory_kwargs['user_cb'](response, factory_kwargs['user_cb_args'])
	return response_hook

def print_response(response, *args, **kwargs):
	print(response)

class WialonSDKClient():

	def __init__(self):
		self.protocol = 'http'
		self.ip = '10.0.2.15'
		self.port = '8021'
		self.login = 'wialon'
		self.password = 'password'
		self.sid = None
		self.jobs = []


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

		rs = grequests.post('{}://{}:{}/oauth/authorize.html'.format(self.protocol, self.ip, self.port), params=data, allow_redirects=False, \
			hooks={'response': [callback_factory(user_cb=self.finish_login, user_cb_args=cb)]})

		j = grequests.send(rs, grequests.Pool(1))
		j.join()
		print('join finished')
		# grequests.gevent.sleep(1)
		# self.jobs.append(job)
		# job.wait()
		# time.sleep(1)


	def finish_login(self, r, cb):
		access_token = get_token(r.headers["Location"])
	
		data = {
			'svc': 'token/login',
			'params': json.dumps({'token': access_token})
		}

		r = requests.post('{}://{}:{}/wialon/ajax.html'.format(self.protocol, self.ip, self.port), params=data)
		self.sid = r.json()['eid']
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


def get_token(url):
	query = url.split('?')[1]
	params = query.split('&')
	for p in params:
		if 'access_token' in p:
			return p.split('=')[1]