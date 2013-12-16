class EventAlreadyExistsException(Exception):
	def __init__(self, error_message):
		self.error_message = error_message
	def __str__(self):
		return repr(self.error_message)

class InvalidEventException(Exception):
	def __init__(self, error_message):
		self.error_message = error_message
	def __str__(self):
		return repr(self.error_message)

class InvalidFacebookEventPageException(Exception):
	def __init__(self, error_message):
		self.error_message = error_message
	def __str__(self):
		return repr(self.error_message)