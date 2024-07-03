#!/usr/bin/bash

pyinstaller --onefile --windowed --icon=logo.ico --add-data="logo.ico;." AutoMouse.py
