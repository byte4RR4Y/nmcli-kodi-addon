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
        print("Fehler beim Abrufen der SSIDs:", e)
        return []
    except Exception as e:
        print("Allgemeiner Fehler:", e)
        return []

def main():
    # SSIDs abrufen
    ssids = get_wifi_ssids()

    # Überprüfe, ob SSIDs gefunden wurden
    if not ssids:
        print("Keine WLAN-Netzwerke gefunden.")
        return

    # Erstelle eine Listeansicht für die SSIDs
    list_items = ssids

    # Zeige Liste der SSIDs in einem Dialog an
    list_dialog = xbmcgui.Dialog()
    selected_index = list_dialog.select('Wählen Sie ein Netzwerk aus', list_items)

    # Überprüfe die Benutzerauswahl
    if selected_index >= 0:
        selected_ssid = ssids[selected_index]

        # Fordern Sie den Benutzer zur Eingabe des Passworts auf
        password = list_dialog.input('Passwort für ' + selected_ssid, '')

        # Überprüfen Sie, ob ein Passwort eingegeben wurde
        if not password:
            list_dialog.notification('Info', 'Leeres Passwort')
            command = ["nmcli", "device", "wifi", "connect", selected_ssid, "password", password]
            subprocess.run(command)
            return

        # Befehl zum Verbinden mit dem ausgewählten Netzwerk
        command = ["nmcli", "device", "wifi", "connect", selected_ssid, "password", password]

        try:
            # Befehl ausführen
            subprocess.run(command)
            list_dialog.notification('Verbindung hergestellt', 'SSID: {}'.format(selected_ssid))
        except subprocess.CalledProcessError as e:
            print("Fehler bei der Verbindung:", e)

if __name__ == "__main__":
    main()
