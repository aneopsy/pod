from dashing.widgets import NumberWidget
from random import randint

users = randint(50, 100)


class NbrVideoWidget(NumberWidget):
	title = 'Number of video'

	def get_value(self):
		global users
		users += 1
		return users

	def get_detail(self):
		global users
		return '{} actives'.format(users/3)
