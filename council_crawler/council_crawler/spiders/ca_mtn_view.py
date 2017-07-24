from templates.legistar_cms import LegistarCms

class Mtn_View(LegistarCms):
	"""
	"""
	name = 'mtn_view'

	def __init__(self, *args, **kwargs):
		super(Mtn_View, self).__init__(*args, city='mountain view', state='ca', **kwargs)
		self.urls = ['https://mountainview.legistar.com/Calendar.aspx']

