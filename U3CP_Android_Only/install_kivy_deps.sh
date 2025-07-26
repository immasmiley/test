#!/bin/bash
echo "Starting Kivy dependency installation..."
echo "This will install all necessary libraries for Kivy."
echo "It may take several minutes and download a significant amount of data."
echo "----------------------------------------------------------------"

pkg install -y python-dev build-essential clang libffi-dev sdl2-dev sdl2-image-dev sdl2-mixer-dev sdl2-ttf-dev pkg-config libjpeg-turbo-dev libpng-dev

echo "----------------------------------------------------------------"
echo "✅ Kivy dependency installation complete."
echo "You can now try running the pip install command again:"
echo "pip install -r requirements_u3cp.txt" 