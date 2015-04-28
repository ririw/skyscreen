import patterns
from plumbum import cli

names = [
	'noise',
	'bands',
	'npnoise',
	'theano.swirl',
	'theano.tripdar',
	'theano.radar',
	'theano.droplet',
	'chaos',
	'fsm.rps',
	'fsm.random_game',
	'fsm.gliders',
	'test.lines',
	'test.grid'
]


class Runner(cli.Application):
	list = False
	display_old = False
	DESCRIPTION = """
	Run the cool applications. You can specify
	an application, or you can just pass no
	argument to run all of them. Press 'q' to
	quit.
	"""

	@cli.switch('-l', help='list all')
	def set_list(self):
		self.list = True

	@cli.switch('--old-display', help='Use the old (broken) display')
	def set_display_old(self):
		self.display_old = True

	def main(self, name=None):
		if self.list:
			print "Here is the list of things you can render"
			for name in names:
				print "\t%s" % name
			return 0
		if name:
			patterns.run_named(name, use_old_display=self.display_old)
		else:
			for name in names:
				patterns.run_named(name, use_old_display=self.display_old)
		return 0


if __name__ == '__main__':
	Runner.run()