# Anleitung

## Was benötigt wird

```
sudo apt-get install libgpiod2
```

## Development

Sollte in dem Projekt programmiert werden, so müssen gewisse Ding beachtet werden.

## Erstellen eines virtuellen Enviroments (venv)

Zuerst muss eine Venv erstellt werden.

```
python3 -m venv /PathToVenv/venv
```

Anschließend eine muss die Venv aktiviert werden (Kapitel: Aktivieren des virtuellen Enviroments)
Zuletzt müssen die nötigen Bibliotheken installiert werden

```
pip install -r requirements.txt
```

### Aktivieren des virtuellen Enviroments (venv)

Damit das Projekt unabhängig von der Umgebung ausgeführt werden kann, wird eine eine venv benutzt. Hier wird die nötige Python Version und alle Bibliotheken hinterlegt.
Wurden die nötigen Rechte verteilt, muss in die Working Directory zur "temp_automation" Directory geändert werden.
Anschließend:

```
source venv/bin/activate
```

Vor dem User müsste nun die venv stehen: (venv) pi@raspberrypi:~/temp_automation $.
Das Beudeutet, dass Python lokal von der venv ausgeführt wird.
**Es sollte in der venv gearbeitet werden!**

### Aktualisierung der Bibliotheken

Eine venv kann nicht bewegt werden. Möchte man den Pfad ändern, so muss die venv gelöscht werden. Um die installierten Bibliotheken zu sichern, wird nachstehender Befehl benutzt.
**Nur verwenden in venv!**

```
pip freeze > requirements.txt
```

Die venv kann dann wie oben zuvor beschrieben mit den gesicherten Bibliotheken erstellt werden.

## Gängige Git Befehle

Laden der Online-Daten (Synchronisieren deines Repos)

```
git pull
```

Hinzufügen deiner erstellten Dateien zu Git (lokal)

```
git add --all
```

Aktualisieren deines Gits (lokal)

```
git commit -a
```

Hochladen deiner Änderungne (Online). Zuvor muss dein lokales Git aktualisiert sein.

```
git push
```
