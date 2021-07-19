import os, sys, subprocess, site, glob					# standard parts of Python install

def get_package_path(package_name):
	''' returns the global or user path for site-packages that contains the package_name'''
	path = ""
	source = "global"
	globalPackages = site.getsitepackages() 			# ['C:\\Program Files\\Python39', 'C:\\Program Files\\Python39\\lib\\site-packages']
	for package in globalPackages:
		if package.__contains__("site-packages"):
			site_path = package							# C:\\Program Files\\Python39\\lib\\site-packages
			
	if os.path.isdir(os.path.join(site_path, package_name)): # found this package_name
		path = site_path
	else:
		site_path = site.getusersitepackages()			#C:\Users\help\AppData\Roaming\Python\Python39\site-packages
		if os.path.isdir(os.path.join(site_path, package_name)): # found
			path = site_path
			source = "user"

	return  path, source 								#return path and whether the package is 'global' or 'user'

def get_scripts_path(path, source):
	''' locate correct path for Scripts '''
	if source == "user": # C:\Users\<user>\AppData\Roaming\Python\Python39\site-packages; C:\Users\<user>\AppData\Roaming\Python\Python39\Scripts
		parts = os.path.split(path)
		scripts_path = os.path.join(parts[0],"Scripts")
	else: # C:\Program Files\Python39\Lib\site-packages; C:\Program Files\Python39\Scripts
		parts = os.path.split(path)
		parts = os.path.split(parts[0])
		scripts_path = os.path.join(parts[0],"Scripts")
	return scripts_path # loction of Scripts varies depending on global or user

def convert(converter, ui_file, py_file):
	''' run the pyuic5.exe: usually done in a cmd propmt '''
	if os.path.exists(converter):
		print(f"Converting {os.path.split(ui_file)[1]}...")
		subprocess.check_call([converter, "-x", ui_file , "-o" , py_file])
	else:
		print(f"pyuic5.exe not found at calculated path: {converter}")

def main():
	''' everything runs from here '''
	cwd = os.getcwd()										# current working directory: convert all .ui files found here
	print(f"Checking for .ui files in {cwd}:")
	ui_files = glob.glob("*.ui")							# list of .ui files (name only, not full path)
	for ui_file in ui_files:
		print(f"\tFound {ui_file}")
	py_files = glob.glob("*.py")							# list of .py files (name only, not full path)
	print("\nChecking for converted .py files:")
	for py_file in py_files:
		if os.path.splitext(py_file)[0] + ".ui" in ui_files:# print any pre-converted .ui to .py files
			print(f"\tFound previously converted {py_file}")	
	path, source = get_package_path("QtDesigner") 			# C:\Users\<user>\AppData\Roaming\Python\Python39\site-packages or Python install folder
	print(f"\nPyQt5 package found in {path} ({source})")
	scripts_path = get_scripts_path(path, source)			# C:\Program Files\Python39\Scripts or C:\Users\<user>\AppData\Roaming\Python\Python39\Scripts
	print(f"Scripts path found at: {scripts_path}\n")
	converter = os.path.join(scripts_path, "pyuic5.exe")	# C:\Users\<user>\AppData\Roaming\Python\Python39\Scripts\pyuic5.exe or C:\Program Files\Python39\Scripts\pyuic5.exe
	list_converted = []										# empty list to store names of converted files
	for ui_file in ui_files:								# iterate all .ui files
		py_file = os.path.splitext(ui_file)[0] + ".py"		# py_file = .py file with same name as .ui -> test.ui found, py_file = test.py
		if not py_file in py_files:							# Look for equivalent, previously converted .py file with same name
			list_converted.append(ui_file)					# add to list of converted files
			ui_file = os.path.join(cwd, ui_file)			# ui_file given full pathname
			py_file = os.path.join(cwd, py_file)			# py_file given full pathname
			convert(converter, ui_file, py_file)			# create .py from .ui
	# Display a list of converted files		
	if len(list_converted) > 0:
		print("The following files were converted from .ui to .py:")
		for file in list_converted:
			print(f"\t{file}")		
		print(f"Move them from {cwd} to a suitable location for their associated projects")
		
	else:
		print("\tNo new .ui files found for conversion")
		
	input("\nEnter to quit")
	
main()