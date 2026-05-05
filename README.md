# AsciiPlayer

Terminal-based music visualizer for Linux (Arch-friendly) with smooth RGB effects, player info, and progress bar.

---

## Features

* Shows current track (title + artist) via `playerctl`
* Smooth RGB color animation
* Single-color mode (configurable)
* ASCII visualizer (animated blocks)
* Time format `00:00 / 03:45`
* Optimized (no lag)
* Works well with transparent terminals (kitty, alacritty)

---

## Installation (Arch Linux)

### 1. Install Python

```bash
sudo pacman -S python
```

Check:

```bash
python --version
```

---

### 2. Install required tools

```bash
sudo pacman -S playerctl
```

`playerctl` is used to get info from your music player (Spotify, VLC, etc.)

---

### 3. Terminal library (curses)

The project uses the built-in Python module `curses`.

* On Arch Linux it is already included with Python
* If something is missing:

```bash
sudo pacman -S ncurses
```

---

### 4. (Optional) Recommended terminal

```bash
sudo pacman -S kitty
```

Run with transparency:

```bash
kitty --background-opacity 0.7
```

---

## Python dependencies

No extra pip libraries required
(uses only built-in modules: `curses`, `json`, `subprocess`, etc.)

---

## Run

```bash
python main.py
```

or:

```bash
chmod +x main.py
./main.py
```

---

## Config

The script automatically creates `config.json`:

```json
{
  "rgb": true,
  "single_color": false,
  "player_color": "cyan"
}
```

---

### Options

| Option         | Description              |
| -------------- | ------------------------ |
| `rgb`          | Smooth rainbow animation |
| `single_color` | Use one color            |
| `player_color` | Color name               |

---

### Available colors

```
black, red, green, yellow, blue, magenta, cyan, white
```

---

## Controls

| Key | Action |
| --- | ------ |
| `q` | Exit   |

---

## Notes

* RGB depends on terminal support (kitty works best)
* Transparency is controlled by the terminal, not Python
* Works with any MPRIS-compatible player

---

## Recommended setup

* Terminal: kitty
* Music: Spotify / VLC
* Optional: tmux for split layout

---

## Future ideas

* Real audio sync (like cava)
* Keyboard controls (pause/next)
* Gradient modes
* Waybar / widget integration

---

## License

MIT
