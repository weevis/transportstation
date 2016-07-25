from pynzb import nzb_parser
from urllib2 import urlopen, URLError

class NZBParse:
	nzbfile = None

	def __init__(self):
		self.nzbfile = None
			

	def readFromURL(self, url, timeout=None):
		try:
			if timeout:
				stream = urlopen(url, timeout)
			else:
				stream = urlopen(url)

			output = stream.read()
		except:
			output = None

		print 'Output from URL: {}'.format(output)
		return output

	def readFromFile(self, filename):
		try:
			contents = open(filename)
			output = contents.read()
		except:
			output = None

		return output

	def parseNZB(self, output):
		try:
			if output is None:
				raise InputError

			nzb_files = nzb_parser.parse(output)

			for nzb_file in nzb_files:
				print 'Subject: {} Date: {} Poster: {} Groups: {}\n'.format(nzb_file.subject, nzb_file.date, nzb_file.poster, nzb_file.groups)
				for segment in nzb_file.segments:
					print 'Segment: {} Message ID: {} Size: {}\n'.format(segment.number, segment.message_id, segment.bytes)

			return nzb_files

		except URLError, TypeError:
			print "Error!"
