from setuptools import setup

with open('README.rst', 'r') as readme_file:
    long_description = readme_file.read()

setup(name='gpiodaemon',
      version='1.6.1',
      description='Raspberry Pi GPIO setup utility for rpi2caster',
      long_description=long_description,
      url='http://github.com/elegantandrogyne/gpiodaemon',
      author='Christophe Slychan',
      author_email='krzysztof.slychan@gmail.com',
      license='GPLv3',
      packages=['gpiodaemon'],
      include_package_data=True,
      package_data={'gpiodaemon': ['systemd/*.service']},
      data_files=[('/etc/systemd/system', ['systemd/gpiodaemon.service'])],
      classifiers=['Development Status :: 5 - Production/Stable',
                   'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3 :: Only',],
      entry_points={'console_scripts':['gpiodaemon = gpiodaemon.__main__:main']},
      install_requires=['gpiozero>=1.2.0'],
      zip_safe=True)
