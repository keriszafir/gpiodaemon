from setuptools import setup

long_description = ('GPIODaemon - reboot and shutdown button handler for Raspberry Pi',
                    '^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^',
                    'This daemon runs on startup as root (via systemd service file ',
                    'and sets up the inputs and outputs for the shutdown and reboot '
                    'buttons and a LED for indicating the system status (ready or powering off).')
setup(name='gpiodaemon',
      version='1.0',
      description='Raspberry Pi GPIO setup utility for rpi2caster',
      long_description=long_description,
      url='http://github.com/elegantandrogyne/gpiodaemon',
      author='Christophe Slychan',
      author_email='krzysztof.slychan@gmail.com',
      license='GPLv3',
      packages=['gpiodaemon'],
      include_package_data=True,
      data_files=[('/etc/systemd/system', ['systemd/gpiodaemon.service'])],
      classifiers=['Development Status :: 2 - Pre-Alpha',
                   'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
                   'Natural Language :: English',
                   'Operating System :: POSIX :: Linux',
                   'Programming Language :: Python :: 3',
                   'Programming Language :: Python :: 2'],
      entry_points={'console_scripts':['gpiodaemon = gpiodaemon.__main__:main']},
      install_requires=['gpiozero>=1.0.0'],
      zip_safe=True)
