from setuptools import setup

setup(
	name = 'menu_parser' , 
	vrsion = '0.1' , 
	py_modules = ['menu_parser'] , 
	install_requires = [
			'Click' , 
	] ,
	entry_points = '''
				[console_scripts]
				 menu = menu_parser:cli
				 ''' ,
	)