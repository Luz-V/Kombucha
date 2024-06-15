#!/bin/bash

echo "
Activation de l'environnement virtuel python."
source .venv/bin/activate
echo "Lancement du serveur Flask Kombucha ...
"
python3 Kombucha_gui.py
