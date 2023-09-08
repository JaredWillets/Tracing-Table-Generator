import os
import string
import webbrowser
def run(htmlString):
	filename = generated_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
	filename = filename+'.html'
	while os.path.isfile(filename):
		filename = generated_string = ''.join(random.choice(string.ascii_lowercase) for _ in range(length))
		filename = filename+'.html'

	f = open(filename,'w')
	f.write(htmlString)
	f.close()
	filename = 'file:///'+os.getcwd()+'/' + filename
	webbrowser.open_new_tab(filename)