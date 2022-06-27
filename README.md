# ZTTT

## Installation
``pip install ZTTT``

## Project Structure

```txt
ZTicTacToe
├── examples
│   └── __init__.py
│
├── src
│   └── ZTTT
│       ├── ZTBase
│       │   ├── __init__.py
│       │   ├── ZTBaseBoard.py
│       │   ├── ZTBaseEngine.py
│       ├── ZTEngines
│       │   ├── __init__.py
│       │   ├── ZTEngineFirst.py
│       │   └── ZTPlayerFirst.py
│       ├── ZTErrors
│       │   ├── __init__.py
│       │   └── ZTErrors.py
│       ├── __init__.py
│       ├── PvC.py
│       └── PvP.py
│
├── tests
│   ├── __init__.py
│   └── test.py
│
├── .gitignore
├── LICENSE.txt
├── README.md
└── setup.py
```

## Usage
Examples will be eventually uploaded
```python
from ZTTT import PvP, PvC

b = PvP()

if b.status:
    b.play(0)  # Player 1 plays in the top Right
    
if b.status:
    b.play(1)  # Player 2 plays in the top Middle
```
