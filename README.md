Installation 

Man benötigt die verschiedenen Bibliotheken damit das Programm läuft, dafür sollte man erstmal versuchen diese über die IDE zu installieren (darüber hovern -> install package), ich empfehle hierfür PyCharm.
Sollte das nicht funktionieren, kann man sich die verschiedenen Pakete manuell installieren

Unter Windows:

```
Bitte selber schauen ob man das Directory wechseln muss zum installieren 

Beispiel zum Wechseln (falls nötig)
cd C:\Users\*username here*\AppData\Local\Programs\Python\Python312\

py -m pip install --upgrade pip
py -m pip install --upgrade Pillow
py -m pip install --upgrade numpy
```

Unter MacOs:

```
Bitte selber schauen ob man das Directory wechseln muss zum installieren 

Danach:
  
python3 -m pip install --upgrade pip
python3 -m pip install --upgrade Pillow
python3 -m pip install --upgrade numpy
```