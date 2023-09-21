import subprocess
import xbmcgui

# Funktion zum Abrufen der SSIDs mithilfe von nmcli
def get_wifi_ssids():
    try:
        # Führen Sie den nmcli-Befehl aus, um die WLAN-Netzwerke abzurufen
        output = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'device', 'wifi', 'list'], universal_newlines=True)
        
        # Teilen Sie die Ausgabe in Zeilen auf und erstellen Sie eine Liste der SSIDs (aus Spalte 1)
        ssids = output.strip().split('\n')
        
        # Entfernen Sie eventuelle führende oder abschließende Leerzeichen
        ssids = [ssid.strip() for ssid in ssids]
        
        return ssids
    except subprocess.CalledProcessError as e:
        print("nmcli Error", e)
        return []
    except Exception as e:
        print("Error", e)
        return []

# SSIDs abrufen
ssids = get_wifi_ssids()

# Erstellen Sie ein Fenster
window = xbmcgui.Window(10000)

# Erstellen Sie eine Listeansicht für die SSIDs
list_items = [ssid for ssid in ssids]

# Zeigen Sie die Liste der SSIDs in einem eigenen Fenster an
list_dialog = xbmcgui.Dialog()
selected_index = list_dialog.select('Choose a network', list_items)

# Überprüfen Sie die Benutzerauswahl
if selected_index >= 0:
   selected_ssid = ssids[selected_index]

   # Fordern Sie den Benutzer zur Eingabe des Passworts auf
   password = list_dialog.input('Password for ' + selected_ssid, '')

# Handhaben Sie die Eingabe des Passworts
if password:
    list_dialog.notification('Info', 'SSID: {} Passwort: {}'.format(selected_ssid, password))
else:
    list_dialog.notification('Info', 'Empty Password')

command = ["nmcli", "device", "wifi", "connect", selected_ssid, "password", password]

# Befehl ausführen
subprocess.run(command)
