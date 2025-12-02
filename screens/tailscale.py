import logging
from PIL import Image

import settings
from libs.tailscale import get_tailscale
from screens import AbstractScreen


class Screen(AbstractScreen):
    """
    Tailscale status screen showing connection info, local/Tailscale IPs,
    exit node status, and connected peers
    """
    tailscale = get_tailscale()
    reload_interval = 30  # Refresh every 30 seconds

    def reload(self):
        # Invalidate cache to get fresh data
        self.tailscale.invalidate_cache()

        self.blank()
        self.draw_titlebar("Tailscale")

        # Try to load Tailscale icon
        try:
            icon = Image.open("images/tailscale.png")
            self.image.paste(icon, (100, 25))
        except FileNotFoundError:
            logging.warning("Tailscale icon not found at images/tailscale.png")

        # Build the status string
        string = ''

        # Connection status
        if self.tailscale.is_connected:
            string += 'Status:    ✓ Connected\n'
        else:
            string += 'Status:    ✗ Disconnected\n'

        # Local IP
        local_ip = self.tailscale.local_ip
        if local_ip:
            string += f'Local:     {local_ip}\n'
        else:
            string += 'Local:     N/A\n'

        # Tailscale IP
        ts_ip = self.tailscale.tailscale_ip
        if ts_ip:
            string += f'Tailscale: {ts_ip}\n'
        else:
            string += 'Tailscale: N/A\n'

        # Exit node status
        exit_status = self.tailscale.exit_node_status
        if exit_status == "Active":
            clients = self.tailscale.active_exit_node_clients
            string += f'Exit Node: ✓ Active ({clients})\n'
        elif exit_status == "Inactive":
            string += 'Exit Node: ✗ Inactive\n'
        else:  # Disabled
            string += 'Exit Node: - Disabled\n'

        # Peers online
        peers = self.tailscale.peers_online
        string += f'Peers:     {peers} online'

        # Draw the status information
        self.text(string, font_size=14, font_name=settings.MONOSPACE_FONT, position=(5, 90), wrap=False)

    def handle_btn_press(self, button_number=1):
        """
        Handle button presses
        Button 1: Reload screen
        """
        if button_number == 1:
            self.reload()
            self.show()
