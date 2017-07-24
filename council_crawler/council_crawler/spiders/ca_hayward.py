from templates.legistar_cms import LegistarCms

class Hayward(LegistarCms):
	"""
	"""
	name = 'hayward'

	def __init__(self, *args, **kwargs):
		super(Hayward, self).__init__(*args, city='hayward', state='ca', **kwargs)
		self.urls = ['https://hayward.legistar.com/Calendar.aspx']

