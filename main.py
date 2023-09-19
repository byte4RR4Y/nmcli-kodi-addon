import subprocess
import xbmc
import xbmcgui

def main():
    # Befehl ausführen, um die Liste der WLAN-Netzwerke zu erhalten
    output = subprocess.check_output(["nmcli", "device", "wifi", "list"]).decode("utf-8")

    # Aufteilen der Ausgabe in Zeilen
    lines = output.splitlines()

    # Initialisieren der Liste für die Netzwerknamen
    netzwerke = []

    # Durchlaufen der Zeilen und Extrahieren der Netzwerknamen
    for line in lines:
        # Zeilen mit Informationen zu WLAN-Netzwerken beginnen normalerweise mit einem * und enthalten die SSID
        if line.startswith("*"):
            parts = line.split()
            if len(parts) >= 2:
                netzwerkname = parts[1]
                netzwerke.append(netzwerkname)

    # Netzwerkliste ausgeben
    kodi_list = xbmcgui.ListItems()

    for netzwerk in netzwerke:
        list_item = xbmcgui.ListItem(netzwerk)
        kodi_list.add(list_item)

    xbmcplugin.addDirectoryItems(handle=int(sys.argv[1]), items=kodi_list, totalItems=len(netzwerke))

    # Überprüfen, ob ein Netzwerk ausgewählt wurde
    selected_item = xbmcplugin.getPluginInfo(int(sys.argv[1]), "selected")

    if selected_item:
        # Den ausgewählten Netzwerknamen und das Passwort hier festlegen
        selected_network = netzwerke[int(selected_item)]
        # Dialogfenster für die Texteingabe anzeigen
        keyboard = xbmcgui.Dialog().input("Passwort", "Geben Sie das Passwort ein:")


        # Befehl für die Verbindung zum Netzwerk
        command = ["nmcli", "device", "wifi", "connect", selected_network, "password", keyboard]

        # Befehl ausführen
        subprocess.run(command)

    xbmcplugin.endOfDirectory(int(sys.argv[1]))

if __name__ == '__main__':
    main()