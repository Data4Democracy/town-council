from templates.legistar_cms import LegistarCms

class San_Mateo(LegistarCms):
	"""
	"""
	name = 'san_mateo'

	def __init__(self, *args, **kwargs):
		super(San_Mateo, self).__init__(*args, city='san mateo', state='ca', **kwargs)
		self.urls = ['https://cosm.legistar.com/Calendar.aspx']

