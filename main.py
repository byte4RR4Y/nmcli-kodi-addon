import subprocess
import xbmcgui

# Funktion zum Abrufen der SSIDs mithilfe von nmcli
def get_wifi_ssids():
    try:
        # Führe den nmcli-Befehl aus, um die WLAN-Netzwerke abzurufen
        output = subprocess.check_output(['nmcli', '-t', '-f', 'SSID', 'device', 'wifi', 'list'], universal_newlines=True)
        
        # Teile die Ausgabe in Zeilen auf und erstelle eine Liste der SSIDs (aus Spalte 1)
        ssids = output.strip().split('\n')
        
        # Entferne eventuell führende oder abschließende Leerzeichen
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

# Erstelle ein Fenster
window = xbmcgui.Window(10000)

# Erstelle eine Listeansicht für die SSIDs
list_items = [ssid for ssid in ssids]

# Zeige Liste der SSIDs in einem eigenen Fenster an
list_dialog = xbmcgui.Dialog()
selected_index = list_dialog.select('Choose a network', list_items)

# Überprüfe die Benutzerauswahl
if selected_index >= 0:
   selected_ssid = ssids[selected_index]

   # Fordern Sie den Benutzer zur Eingabe des Passworts auf
   password = list_dialog.input('Password for ' + selected_ssid, '')

# Eingabe des Passworts
if password:
    list_dialog.notification('Info', 'SSID: {} Passwort: {}'.format(selected_ssid, password))
else:
    list_dialog.notification('Info', 'Empty Password')

command = ["nmcli", "device", "wifi", "connect", selected_ssid, "password", password]

# Befehl ausführen
subprocess.run(command)
