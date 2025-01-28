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
```python
from game import CaboError
# Error Code, Nachricht optional
raise CaboError(0, "message")
```

### ArgumentError
```python
from game import ArgumentError
def methode(argument) -> None: # argument muss positive sein
    if argument < 0:
        # Error Code | Nachricht, falsches Argument, richtiges Argument | alles optional
        raise ArgumentError(0, "message", argument, 1)
```
### StateError
```python
from game import StateError
# Error Code, Nachricht optional
raise StateError(0, "message")
```
### Error-Codes
- CaboError:
  - 0
- ArgumentError:
  - 0
- StateError:
  - 0