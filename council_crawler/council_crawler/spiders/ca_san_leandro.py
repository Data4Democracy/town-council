from templates.legistar_cms import LegistarCms

class San_Leandro(LegistarCms):
	"""
	"""
	name = 'san_leandro'

	def __init__(self, *args, **kwargs):
		super(San_Leandro, self).__init__(*args, city='san leandro', state='ca', **kwargs)
		self.urls = ['https://sanleandro.legistar.com/Calendar.aspx']

