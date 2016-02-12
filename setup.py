from setuptools import setup

setup(
	name = 'menu_parser' , 
	vrsion = '0.1' , 
	description = 'Tool to read images ,images formatted like standard restaurant-menu'
	author = 'Amit Kushwaha'
	author_email = 'amit_kushwaha@outlook.com'
	url = ''
	download_url = ''
	keywords = ['image reader' , 'menu_parser' , 'menu reader']
	py_modules = ['menu_parser'] , 
	include_package_data=True,
    license = 'MIT License',
	install_requires = [
			'Click' , 
	] ,
	entry_points = '''
				[console_scripts]
				 menu = menu_parser:cli
				 ''' ,
	)