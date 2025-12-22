#!/bin/bash

echo "   ____       _   ___      _ 
  / __ \_  __/ | / (_)____(_)
 / / / / |/_/  |/ / / ___/ /
/ /_/ />  </ /|  / / /  / /
\____/_/|_/_/ |_/_/_/  /_/
"

# Install yay (AUR helper)
sudo pacman -Syu --needed --noconfirm base-devel git
exit
git clone https://aur.archlinux.org/yay.git ~/yay
cd ~/yay
makepkg -si
rm -rf ~/yay

# Install packages

cd ~/0xNiri
yay -S --needed --noconfirm - < packages.list

# Install optional packages

yay -S --needed - < optional-packages.list

# Set fish as default shell

chsh -s /bin/fish

# Setup config files

cp -r ~/0xNiri/.config/. ~/.config/

# Move scripts to ~/.local/share/bin

mkdir -p ~/.local/share/bin
cp -r ~/0xNiri/bin/. ~/.local/share/bin

# Add ~/.local/share/bin to PATH variable

fish_add_path -a ~/.local/share/bin

# Start Essential services

services=(cliphist niri-screen-time nirius polkit-gnome swaybg swww-wallpaper syshud waybar xwayland-satellite)

for i in ${services[@]}; do
    systemctl --user add-wants niri.service "$i"
    systemctl --user start "$i"
done

# Start Optional services

optional_servies=(auto-hide-waybar autotrash easyeffects kdeconnect-indicator wlsunset)

for i in ${optional_servies[@]}; do
    read -rp "Do you want to start $i.service? [y/N]: " -n 1
    echo
    if [[ $REPLY =~ ^[Yy]$ ]]; then
        systemctl --user add-wants niri.service "$i"
        systemctl --user start "$i"
    fi
done

# Set Wallpaper

set-wallpaper ~/.config/niri/wallpaper.jpg

# Install & set GTK Theme

git clone https://github.com/Fausto-Korpsvart/Catppuccin-GTK-Theme.git ~/themes
bash ~/themes/themes/install.sh --tweaks macos float -t lavender -l
gsettings set org.gnome-desktop.interface gtk-theme "'Catppuccin-Lavender-Dark'"
trash ~/themes

# Install & set Icon theme

papirus-folders -C cat-latte-lavender --theme Papirus-Light
gsettings set org.gnome.desktop.interface icon-theme "'Papirus-Light'"

# Customize fish shell

fisher install IlanCosman/tide@6

# Set profile picture in gtklock

read -rp "Do you want to set profile picture? [y/N]" -n 1
if [[ $REPLY =~ ^[yY]$ ]]; then
    mugshot
fi

# Some useful stuffs

echo
echo "=> Go through below locations to make your life easier"
echo

echo "Configs: ~/.config"
echo "Scripts: ~/.local/share/bin"
echo "Services: ~/.config/systemd/user"
echo

toilet -t -f larry3d "Enjoy 0xNiri!"
