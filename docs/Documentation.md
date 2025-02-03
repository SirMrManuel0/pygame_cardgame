# Dokumentation

## Inhalt:
1. [Errors](#Errors)
2. Diagramm


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
- StateError:

### ArgumentError-1
Dieser Fehler wird von der Funktion get_abs_path ausgelöst.
Er impliziert einen falschen relativen Pfad.
