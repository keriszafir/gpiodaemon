"""gpiodaemon - a daemon for setting up and tearing down the Raspberry Pi
GPIO sysfs interface on given pins. This is supposed to
run as a privileged user on startup. The daemon handles shutdown and reboot
button presses."""
import os
import signal
import gpiozero
import atexit

# Set up the GPIO numbers:
sensor_gpio = 17  # photocell input
shutdown_button_gpio = 24  # shutdown button input, pulled up
reboot_button_gpio = 23  # reboot button input, pulled up
emergency_gpio = 22  # emergency stop button input, pulled up
led_gpio = 18  # "system ready" LED output


def shutdown():
    """Shut the system down"""
    ready_led.blink(on_time=0.5, off_time=0.5, n=3, background=False)
    ready_led.on()
    os.system('shutdown -h now')


def reboot():
    """Shut the system down"""
    ready_led.blink(on_time=0.5, off_time=0.5, n=3, background=False)
    ready_led.on()
    os.system('shutdown -r now')


def gpio_setup(gpio_number):
    """Export the machine cycle sensor GPIO output as file,
    so that rpi2caster can access it without root privileges
    """
    # Set up the GPIO
    os.system('echo "%i" > /sys/class/gpio/export' % gpio_number)
    os.system('echo "in" > /sys/class/gpio/gpio%i/direction' % gpio_number)
    # Enable generating interrupts on rising and falling edges:
    os.system('echo "both" > /sys/class/gpio/gpio%i/edge' % gpio_number)


def gpio_cleanup():
    """Cleanup after exit"""
    ready_led.blink(on_time=0.2, off_time=0.2, n=3, background=False)
    os.system('echo "%i" > /sys/class/gpio/unexport' % sensor_gpio)
    os.system('echo "%i" > /sys/class/gpio/unexport' % emergency_gpio)


def signal_handler(signum, frame):
    """Signal handler for SIGTERM and SIGINT"""
    exit()


def main():
    """Main function"""
    try:
        # Initialize the LED and buttons
        global ready_led
        ready_led = gpiozero.LED(led_gpio, initial_value=True)
        shutdown_button = gpiozero.Button(shutdown_button_gpio, hold_time=2)
        reboot_button = gpiozero.Button(reboot_button_gpio, hold_time=2)
        # Set up a sysfs interface for gpios, guarantee tearing it down on exit
        gpio_setup(sensor_gpio)
        gpio_setup(emergency_gpio)
        atexit.register(gpio_cleanup)
        # Do nothing (and wait for interrupts from buttons)
        shutdown_button.when_held = shutdown
        reboot_button.when_held = reboot
        # Exit gracefully when received SIGTERM or SIGINT (on exit)
        signal.signal(signal.SIGINT, signal_handler)
        signal.signal(signal.SIGTERM, signal_handler)
        signal.pause()
    except (OSError, PermissionError, RuntimeError):
        print('You must run this program as root!')
        exit()
    except (KeyboardInterrupt, EOFError):
        exit()


if __name__ == '__main__':
    main()
