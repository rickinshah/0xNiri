```text
   ____       _   ___      _ 
  / __ \_  __/ | / (_)____(_)
 / / / / |/_/  |/ / / ___/ /
/ /_/ />  </ /|  / / /  / /
\____/_/|_/_/ |_/_/_/  /_/
```

Personal dotfiles for the [Niri](https://github.com/YaLTeR/niri) Wayland compositor.

> Theme: [Catppuccin Mocha](https://github.com/catppuccin)

## Preview

https://github.com/user-attachments/assets/8d2dd5dd-cd29-47e0-b2bc-d6dafb082748

## Features

- Waybar auto-hide script.
- Consistent **Catppuccin Mocha** theme across all apps.
- Full desktop-like experience on a minimal **Niri** setup.

## Tools & Utilities

| Category | Application |
| - | - |
| Compositor | [`niri`](https://github.com/YaLTeR/niri) |
| Bar | [`waybar`](https://github.com/Alexays/Waybar) |
| Terminal | [`kitty`](https://github.com/kovidgoyal/kitty) |
| Notification | [`swaync`](https://github.com/ErikReider/SwayNotificationCenter) |
| Wallpaper Manager | [`swaybg`](https://github.com/swaywm/swaybg) / [`swww`](https://github.com/LGFae/swww) |
| Clipboard Manager | [`cliphist`](https://github.com/sentriz/cliphist) |
| Launcher | [`fuzzel`](https://codeberg.org/dnkl/fuzzel) |
| Power Menu | [`wlogout`](https://github.com/ArtsyMacaw/wlogout) |
| Screen Locker | [`gtklock`](https://github.com/jovanlanik/gtklock) |
| On-Screen Display | [`syshud`](https://github.com/System64fumo/syshud) |
| File Manager | [`thunar`](https://gitlab.xfce.org/xfce/thunar) / [`yazi`](https://github.com/sxyazi/yazi) |
| Shell | [`fish`](https://github.com/fish-shell/fish-shell) |
| Display Manager | [`ly`](https://github.com/fairyglade/ly) |

## Installation

> [!NOTE]
> This setup is intended for Arch-based distributions.

### Automated [Under Developement]

> [!WARNING]
> Manual Installation is recommended. This is still under development.

> [!NOTE]
> This may overwrite your existing config. Backup your old config files.

```bash
git clone https://github.com/rickinshah/0xNiri.git ~/0xNiri
cd ~/0xNiri
./install.sh
```

### Manual

#### 1. Clone the repo
```bash
git clone https://github.com/rickinshah/0xNiri.git ~/0xNiri
cd ~/0xNiri
```


#### 2. Install required packages

##### Install `yay`
```bash
sudo pacman -S --needed base-devel git
git clone https://aur.archlinux.org/yay.git ~/yay
cd ~/yay
makepkg -si
rm -rf ~/yay
```

##### Install packages
```bash
yay -S --needed --noconfirm - < ~/0xNiri/packages.list
```

##### Install optional packages
```bash
yay -S --needed --noconfirm - < ~/0xNiri/optional-packages.list
```

#### 3. Set `fish` as default shell
```bash
chsh -s /bin/fish
```

#### 4. Setup config files
```fish
cp -r ~/0xNiri/.config/. ~/.config/
```

#### 5. Setup scripts

##### Move scripts to `~/.local/share/bin`
```fish
mkdir -p ~/.local/share/bin
cp -r ~/0xNiri/bin/. ~/.local/share/bin
```

##### Add `~/.local/share/bin` to `PATH` variable
```fish
fish_add_path -a ~/.local/share/bin
```

> [!WARNING]
> Some keybindings or systemd services may not work if `~/.local/share/bin` is not added to your `PATH` variable.

#### 6. Start the essential startup applications. [Refer to this section](#startup-applications)

#### 7. `Logout` or `Restart`

#### 8. Post Installation

##### Set Wallpaper
```fish
set-wallpaper ~/.config/niri/wallpaper.jpg
```

##### Install & set GTK Theme
```fish
git clone https://github.com/Fausto-Korpsvart/Catppuccin-GTK-Theme.git ~/themes
bash ~/themes/themes/install.sh --tweaks macos float -t lavender -l
gsettings set org.gnome.desktop.interface gtk-theme "'Catppuccin-Lavender-Dark'"
trash ~/themes
```

##### Install & set Icon Theme
```fish
papirus-folders -C cat-latte-lavender --theme Papirus-Light
gsettings set org.gnome.desktop.interface icon-theme "'Papirus-Light'"
```

##### Customize `fish` shell
```fish
fisher install IlanCosman/tide@v6
```

##### Set profile picture in `gtklock`
```fish
mugshot
```

## Startup Applications

Startup applications are managed using `systemd` — as recommended in [official Niri documentation](https://github.com/YaLTeR/niri/wiki/Example-systemd-Setup)

Custom unit files are stored in: `~/.config/systemd/user`

### Essential Services

| Service | Purpose |
| - | - |
| `cliphist` | Clipboard Manager |
| `niri-screen-time` | Screen Time |
| `nirius` | Nirius |
| `polkit-gnome` | Polkit auth agent |
| `swaybg` | Blur Wallpaper(overview mode) |
| `swww-wallpaper` | Wallpaper |
| `syshud` | OSD for volume/brightness |
| `waybar` | Status bar |
| `xwayland-satellite` | Xwayland support |

### Optional Services

| Service | Purpose |
| - | - |
| `auto-hide-waybar` | Auto hide waybar |
| `autotrash` | Removes trash items older than 30 days |
| `kdeconnect-indicator` | KDE Connect |
| `wlsunset` | Night Light |

#### Enable services with:
```fish
systemctl --user add-wants niri.service <service>.service
```

#### For example:
```fish
systemctl --user add-wants niri.service waybar.service
systemctl --user add-wants niri.service syshud.service
```

## Useful Locations

#### Go through following locations to make your life easier.

- Configs - `~/.config`
- Scripts - `~/.local/share/bin`
- Services - `~/.config/systemd/user`

## Credits

- [Wallpapers](https://github.com/orangci/walls-catppuccin-mocha)
- [GTK Theme](https://github.com/Fausto-Korpsvart/Catppuccin-GTK-Theme)
- [Icon Theme](https://github.com/catppuccin/papirus-folders)
