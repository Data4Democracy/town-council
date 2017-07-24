from templates.legistar_cms import LegistarCms

class Cupertino(LegistarCms):
	"""
	"""
	name = 'cupertino'

	def __init__(self, *args, **kwargs):
		super(Cupertino, self).__init__(*args, city='cupertino', state='ca', **kwargs)
		self.urls = ['https://cupertino.legistar.com/Calendar.aspx']

