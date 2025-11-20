# 0xNiri

Personal dotfiles for the [Niri](https://github.com/YaLTeR/niri) Wayland compositor.

> Theme: [Catppuccin Mocha](https://github.com/catppuccin)

## Preview

https://github.com/user-attachments/assets/1590abcc-2be2-49b4-9ed3-ec0d947c69c7

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

### Clone the repo
```bash
git clone https://github.com/rickinshah/0xNiri.git ~/.dotfiles
cd ~/.dotfiles
```

### Installation

#### 1. Install required packages

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
cd ~/.dotfiles
yay -S --needed --noconfirm $(cat packages.txt)
```

##### Install optional packages
```bash
yay -S --needed --noconfirm $(cat optional-packages.txt)
```

#### 2. Set `fish` as default shell
```bash
chsh -s /bin/fish
```

#### 3. Setup config files
```fish
cp -r ~/.dotfiles/.config/. ~/.config/
```

#### 4. Setup scripts

##### Move scripts to `~/.local/share/bin`
```fish
mkdir -p ~/.local/share/bin
cp -r ~/.dotfiles/bin/. ~/.local/share/bin
```

##### Add `~/.local/share/bin` to `PATH` variable
```fish
fish_add_path -a ~/.local/share/bin
```

##### Remove `~/.dotfiles`
```fish
trash ~/.dotfiles
```

> [!WARNING]
> Some keybindings or systemd services may not work if `~/.local/share/bin` is not added to your `PATH` variable.

#### 5. Start the essential startup applications. [Refer to this section](#startup-applications)

#### 6. `Logout` or `Restart`

### Post Installation [Optional]

#### Set Wallpaper
```fish
set-wallpaper ~/.config/niri/wallpaper.jpg
```

#### Install & set GTK Theme
```fish
git clone https://github.com/Fausto-Korpsvart/Catppuccin-GTK-Theme.git ~/themes
bash ~/themes/themes/install.sh --tweaks macos float -t lavender -l
gsettings set org.gnome.desktop.interface gtk-theme "'Catppuccin-Lavender-Dark'"
trash ~/themes
```

#### Install & set Icon Theme
```fish
papirus-folders -C cat-latte-lavender --theme Papirus-Light
gsettings set org.gnome.desktop.interface icon-theme "'Papirus-Light'"
```

#### Customize `fish` shell
```fish
fisher install IlanCosman/tide@v6
```

#### Install `niri-screen-time`
```fish
sudo pacman -S go
go install github.com/probeldev/niri-screen-time@latest
fish_add_path -a $(go env GOPATH)/bin
```

#### Set profile picture in `gtklock`
```fish
mv ~/.dotfiles/.face.jpg ~/.face
```

## Startup Applications

Startup applications are managed using `systemd` — as recommended in [official Niri documentation](https://github.com/YaLTeR/niri/wiki/Example-systemd-Setup)

Custom unit files are stored in: `~/.config/systemd/user`

### Essential Services

| Service | Purpose |
| - | - |
| `syshud.service` | OSD for volume/brightness |
| `cliphist.service` | Clipboard Manager |
| `polkit-gnome.service` | Polkit auth agent |
| `swaybg.service` | Blur Wallpaper(overview mode) |
| `swww-wallpaper.service` | Wallpaper |
| `waybar.service` | Status bar |
| `xwayland-satellite.service` | Xwayland support |
| `nirius.service` | Nirius |

### Optional Services

| Service | Purpose |
| - | - |
| `auto-hide-waybar.service` | Auto hide waybar |
| `check-updates.service` | Check updates and notify on startup |
| `kdeconnect-indicator.service` | KDE Connect |
| `niri-screen-time.service` | Screen Time |
| `wlsunset.service` | Night Mode |

Enable services with:
```fish
systemctl --user add-wants niri.service <service>.service
```

For example:
```fish
systemctl --user add-wants niri.service waybar.service
systemctl --user add-wants niri.service syshud.service
```

## Credits

- [Wallpapers](https://github.com/orangci/walls-catppuccin-mocha)
- [GTK Theme](https://github.com/Fausto-Korpsvart/Catppuccin-GTK-Theme)
- [Icon Theme](https://github.com/catppuccin/papirus-folders)
