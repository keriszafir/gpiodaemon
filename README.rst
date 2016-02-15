GPIODaemon - reboot and shutdown button handler for Raspberry Pi
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

This daemon runs on startup as root (via systemd service file)
and sets up the inputs and outputs for the shutdown and reboot
buttons and a LED for indicating the system status (ready or powering off).

