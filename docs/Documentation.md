# Dokumentation

## Inhalt:
1. [Voraussetzungen](#voraussetzungen)
2. [Errors](#Errors)
3. Diagramm
4. [statische Funktionen](#statische-funktionen)

## Voraussetzungen
Alle benötigten Packages sind in `requirements` gelistet.
Um alle auf einmal zu installieren, benutze den Befehl:
````
pip install requirements
````

## Errors:
- [CaboError](#CaboError)
- [ArgumentError](#ArgumentError)
- [StateError](#StateError)
- [Error Codes](#Error-Codes)


### CaboError
CaboError ist ein standard Error, der aus jeglichen Gründen aufgerufen werden kann.
#
```python
from game import CaboError
# Error Code, Nachricht optional
raise CaboError(0, "message")
```

### ArgumentError
ArgumentError ist ein spezifischer Error, der nur bei schlechten Argumenten ausgelöst wird.
Sie werden an dem Anfang einer Funktion oder nach einiger Logik ausgelöst.
#
```python
from game import ArgumentError
def methode(argument) -> None: # argument muss positive sein
    if argument < 0:
        # Error Code | Nachricht, falsches Argument, richtiges Argument | alles optional
        raise ArgumentError(0, "message", argument, 1)
```
### StateError
StateError ist ein spezifischer Error, der ausgelöst wird, wenn eine Funktion ohne bestimmte Voraussetzungen aufgerufen wird.
#
```python
from game import StateError
# Error Code, Nachricht optional
raise StateError(0, "message")
```
### Error-Codes
- CaboError:
- ArgumentError:
  - [1](#ArgumentError-1)
  - [2](#ArgumentError-2)
  - [3](#ArgumentError-3)
  - [4](#ArgumentError-4)
- StateError:

### ArgumentError 1
Dieser Fehler wird von der Funktion `get_path_abs` ausgelöst. 
Er impliziert einen falschen relativen Pfad.

### ArgumentError 2
Dieser Fehler wird von der Funktion `get_path_resource` ausgelöst.
Er bedeutet, dass ein nicht String in den `args` ist.

### ArgumentError 3
Dieser Fehler wird von der Funktion `get_path_resource` ausgelöst.
Er impliziert einen Schlüssel, der nicht in resources ist, in den `args`.
Es kann sein, dass der in `args` gegebene Weg zu weit geht. 

### ArgumentError 4
Dieser Fehler wird von der Funktion `get_path_resource` ausgelöst.
Er bedeutet, dass die `args` nicht in einem Path enden.
Es kann sein, dass welche vergessen wurden oder der Eintrag in `resources.json` falsch ist.

## statische Funktionen
- [get_path_abs](#get_path_abs)
- [get_path_resource](#get_path_resource)
- run

### get_path_abs
Diese Funktion erwartet einen relativen Pfad und gibt den absoluten Pfad wieder. Der Ankerpunkt ist der `game` Ordner.

ArgumentError: [1](#argumenterror-1)

### get_path_resource
Diese Funktion erwartet die Reihenfolge an Schlüsseln, unter der der Pfad der resource in `resources.json` gespeichert ist.

ArgumentError: [2](#argumenterror-2), [3](#argumenterror-3), [4](#argumenterror-4)