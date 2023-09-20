import subprocess
import xbmcgui



networkname = xbmcgui.Dialog().input('Enter Networkname', '')
password = xbmcgui.Dialog().input('Enter Password', '')

# Befehl für die Verbindung zum Netzwerk
command = ["nmcli", "device", "wifi", "connect", networkname, "password", password]

# Befehl ausführen
subprocess.run(command)
