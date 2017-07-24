from templates.legistar_cms import LegistarCms

class Sunnyvale(LegistarCms):
	"""
	"""
	name = 'sunnyvale'

	def __init__(self, *args, **kwargs):
		super(Sunnyvale, self).__init__(*args, city='sunnyvale', state='ca', **kwargs)
		self.urls = ['https://sunnyvaleca.legistar.com/Calendar.aspx']

