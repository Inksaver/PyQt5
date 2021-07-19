import sys, subprocess
try:
	import pip
	subprocess.check_call([sys.executable, '-m', 'pip', '--version'])
except ImportError:
	print("Pip not present.")
	
input("Enter to quit")