"""gpiodaemon - a daemon for setting up and tearing down the Raspberry Pi
GPIO sysfs interface on given pins. This is supposed to
run as a privileged user on startup. The daemon handles shutdown and reboot
button presses."""
from subprocess import run
import io
import signal
import configparser
import gpiozero

# Set up the constants:
DEFAULT_SENSOR_GPIO = 17  # photocell input
DEFAULT_SHUTDOWN_GPIO = 24  # shutdown button input, pulled up
DEFAULT_REBOOT_GPIO = 23  # reboot button input, pulled up
DEFAULT_STOP_GPIO = 22  # emergency stop button input, pulled up
DEFAULT_LED_GPIO = 18  # "system ready" LED output
CONFIG_PATH = '/etc/rpi2caster.conf'


class ExitProgram(Exception):
    """Raised to exit the program"""
    pass


def get_config(section_name, option_name, default_value, datatype=int):
    """Gets a value for a given parameter from a given name"""
    try:
        with io.open(CONFIG_PATH, 'r'):
            cfg = configparser.ConfigParser()
            cfg.read(CONFIG_PATH)
            return datatype(cfg.get(section_name, option_name))
    except (IOError, FileNotFoundError, TypeError, ValueError, AttributeError,
            configparser.NoSectionError, configparser.NoOptionError):
        # No option found in this config file - tr
        return default_value


def main():
    """Main function"""
    # Define subroutines
    def blink(time=0.5, num=3):
        """Blink the LED"""
        ready_led.blink(on_time=time, off_time=time, n=num, background=False)
        ready_led.on()

    def shutdown():
        """Shut the system down"""
        print('Shutdown button pressed')
        blink()
        run(['shutdown', '-h', 'now'])

    def reboot():
        """Shut the system down"""
        print('Reboot button pressed')
        blink()
        run(['shutdown', '-r', 'now'])

    def gpio_setup(*args):
        """Export the machine cycle sensor GPIO output as file,
        so that rpi2caster can access it without root privileges
        """
        path = '/sys/class/gpio/'
        for gpio in args:
            # Export the GPIO to sysfs kernel interface
            with io.open(path + 'export', 'w') as export:
                export.write('%s' % gpio)
            # Enable generating interrupts on rising and falling edges:
            with io.open(path + 'gpio%s/direction' % gpio, 'w') as direction:
                direction.write('in')
            # Enable generating interrupts on rising and falling edges:
            with io.open(path + 'gpio%s/edge' % gpio, 'w') as edge:
                edge.write('both')

    def gpio_teardown(*args):
        """Unexport the GPIO in sysfs"""
        for gpio in args:
            with io.open('/sys/class/gpio/unexport', 'w') as unexport_file:
                unexport_file.write('%s' % gpio)

    def signal_handler(*_):
        """Signal handler for SIGTERM and SIGINT"""
        raise ExitProgram

    # Set up the GPIOs, exit if failed
    try:
        # Get the configuration values for buttons, sensor and LED
        sensor_gpio = get_config('Interface', 'sensor_gpio',
                                 DEFAULT_SENSOR_GPIO)
        led_gpio = get_config('Interface', 'led_gpio', DEFAULT_LED_GPIO)
        emergency_gpio = get_config('Interface', 'emergency_stop_gpio',
                                    DEFAULT_STOP_GPIO)
        shutdown_button_gpio = get_config('Interface', 'shutdown_gpio',
                                          DEFAULT_SHUTDOWN_GPIO)
        reboot_button_gpio = get_config('Interface', 'reboot_gpio',
                                        DEFAULT_REBOOT_GPIO)
        sensor_used = get_config('Interface', 'sensor', 'simulation', str)
        ready_led = gpiozero.LED(led_gpio, initial_value=True)
        # We know GPIO pins so we can create gpiozero objects for them...
        shutdown_button = gpiozero.Button(shutdown_button_gpio, hold_time=2)
        reboot_button = gpiozero.Button(reboot_button_gpio, hold_time=2)
        # Set up a sysfs interface for GPIOs
        if sensor_used == 'sysfs':
            gpio_setup(sensor_gpio, emergency_gpio)
    except (OSError, PermissionError, RuntimeError):
        print('You must run this program as root!')
        return 1
    # All GPIOs are now set up; start waiting for keypress
    try:
        # Set up the buttons to use callbacks
        shutdown_button.when_held = shutdown
        reboot_button.when_held = reboot
        # Exit gracefully when received SIGTERM or SIGINT (on exit)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.pause()
    except (KeyboardInterrupt, EOFError, ExitProgram):
        # Skip to the "finally" section
        pass
    finally:
        # Teardown of the configured GPIO interface
        gpio_teardown(sensor_gpio, emergency_gpio)
        blink(0.2)
    # Exit successfully
    return 0


if __name__ == '__main__':
    main()
