import json

default_config_text = '''{
	"settings_preset": "Wialon Hosting",
	"request_preset": "Search units"
}'''

default_config = json.loads(default_config_text)

class devtools_config():
	def __init__(self, config_path):
		self.config_path = config_path

	def get(self, config_key):
		config_value = self.try_file(config_key)
		if config_value is None:
			config_value = self.try_default(config_key)
		return config_value

	def try_default(self, config_key):
		return self.config_try(default_config, config_key)

	def try_file(self, config_key):
		file_config = None
		with open(self.config_path) as config:
			file_config = json.load(config)
		return self.config_try(file_config, config_key)

	def config_try(self, config, config_key):
		if not config or not config_key:
			return None
		keys = config_key.split('.')
		value = config
		for k in keys:
			if k in value:
				value = value[k]
			else:
				return None

		return value

if __name__ == "__main__":
	dc = devtools_config('dt.conf')
	print(dc.get('settings_preset'))