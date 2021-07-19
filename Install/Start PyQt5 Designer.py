import os, sys, subprocess, site 					# standard parts of Python install

def is_pip_installed():
	success = True
	try:
		import pip
		subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
	except ImportError:
		success = False
		
	return success

def importPyQt5():
	''' try to import or install PyQt5'''
	try:
		print("Checking for PyQt5")
		import PyQt5
		print("PyQt5 found")
	except ImportError:
		print("Attempting to install PyQt5")
		subprocess.check_call([sys.executable, "-m", "pip", "install", 'PyQt5'])
		
def importPyQt5Designer():
	''' try to import or install PyQt5Designer'''
	try:
		print("Checking for PyQt5Designer")
		import PyQt5Designer
		print("PyQt5Designer found")
	except ImportError:
		print("Attempting to import PyQt5Designer")
		subprocess.check_call([sys.executable, "-m", "pip", "install", 'PyQt5Designer'])
	
def is_lib_installed(lib_name):
	''' check if a library is already installed'''
	try:
		from pip._internal.operations import freeze		# will work as long as pip is installed
	except ImportError:  # pip < 10.0
		from pip.operations import freeze	
	libs = freeze.freeze()
	found = False
	for lib in libs:
		if lib.__contains__(lib_name):
			found = True
	
	return found

def get_package_path(package_name):
	''' returns the global or user path for site-packages that contains the package_name'''
	path = ""
	globalPackages = site.getsitepackages() # ['C:\\Program Files\\Python39', 'C:\\Program Files\\Python39\\lib\\site-packages']
	for package in globalPackages:
		if package.__contains__("site-packages"):
			site_path = package	# C:\\Program Files\\Python39\\lib\\site-packages
			
	if os.path.isdir(os.path.join(site_path, package_name)): # found this package_name
		path = site_path
	else:
		site_path = site.getusersitepackages()	#C:\Users\help\AppData\Roaming\Python\Python39\site-packages
		if os.path.isdir(os.path.join(site_path, package_name)): # found
			path = site_path

	return os.path.join(path, package_name) # return full path including package

def main():
	if not is_pip_installed:
		print("Pip is not installed. Run get-pip.py first, then try again")
		input("Enter to quit")
	else:		
		if not is_lib_installed("PyQt5"):				# PyQt5 not installed
			importPyQt5()								# so install it!
		if is_lib_installed("PyQt5"):					# PyQt5 now installed, just checking
			if not is_lib_installed("Designer"): 		# PyQt5Designer not installed
				importPyQt5Designer()					# so install it!
			
		if is_lib_installed("Designer"): 				# designer installed?
			path = get_package_path("QtDesigner") 		# C:\Users\<user>\AppData\Roaming\Python\Python39\site-packages\QtDesigner
			file = os.path.join(path, "designer.exe")	# C:\Users\<user>\AppData\Roaming\Python\Python39\site-packages\QtDesigner\designer.exe
			subprocess.Popen(file)						# start QtDesigner
		else:
			print("Unable to locate Qt Designer")
			input("Enter to continue")
	
main()



	
