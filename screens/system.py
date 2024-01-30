import logging
import os

import humanize
from PIL import Image

import settings
from libs import system
from screens import AbstractScreen
from settings import LOGO


class Screen(AbstractScreen):
    system = system.get_system()

    def reload(self):
        self.blank()
        self.draw_titlebar("System")

        if LOGO:
            logo = Image.open(LOGO)
        else:
            logo = Image.open(self.system.icon)
        self.image.paste(logo, (100, 25))

        string = self.system.model + '\n'
        self.text(string, font_size=14, font_name=settings.BOLD_FONT, position=(5, 75), wrap=False)

        string = ''

        string += 'OS:       ' + self.system.dist + '\n'

        string += 'Local IP: ' + str(self.system.local_ipv4_address) + '\n'
        string += 'Node:     ' + self.system.node + '\n'

        string += 'CPU Temp: ' + str(round(self.system.temperature)) + '°\n'
        string += 'Uptime:   ' + humanize.naturaldelta(self.system.uptime)

        self.text(string, font_size=14, font_name=settings.MONOSPACE_FONT, position=(5, 90), wrap=False)

    def handle_btn_press(self, button_number=1):
        if button_number == 1:
            self.reload()
            self.show()
        elif button_number == 2:
            logging.info("Rebooting...")
            self.blank()
            self.text("Rebooting...", font_size=30)
            self.show()
            os.system("sudo systemctl reboot")
