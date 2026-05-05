#!/usr/bin/env python3

import curses
import time
import random
import subprocess
import colorsys
import json
import os

CONFIG_FILE = "config.json"

default_config = {
    "rgb": True,
    "single_color": False,
    "player_color": "cyan"
}

color_map = {
    "black": curses.COLOR_BLACK,
    "red": curses.COLOR_RED,
    "green": curses.COLOR_GREEN,
    "yellow": curses.COLOR_YELLOW,
    "blue": curses.COLOR_BLUE,
    "magenta": curses.COLOR_MAGENTA,
    "cyan": curses.COLOR_CYAN,
    "white": curses.COLOR_WHITE
}

# --- безопасная загрузка конфига
def load_config():
    try:
        if not os.path.exists(CONFIG_FILE):
            raise Exception()

        with open(CONFIG_FILE, "r") as f:
            data = f.read().strip()
            if not data:
                raise Exception()
            return json.loads(data)

    except:
        with open(CONFIG_FILE, "w") as f:
            json.dump(default_config, f, indent=4)
        return default_config


def get_player_info():
    try:
        status = subprocess.getoutput("playerctl status")
        title = subprocess.getoutput("playerctl metadata title")
        artist = subprocess.getoutput("playerctl metadata artist")
        position = float(subprocess.getoutput("playerctl position"))
        length = float(subprocess.getoutput("playerctl metadata mpris:length")) / 1_000_000
        return status, title, artist, position, length
    except:
        return "Stopped", "No Track", "", 0, 1


# --- формат времени 00:00
def format_time(seconds):
    seconds = int(seconds)
    m = seconds // 60
    s = seconds % 60
    return f"{m:02d}:{s:02d}"


def init_colors():
    curses.start_color()
    curses.use_default_colors()

    for i in range(0, 8):
        curses.init_pair(i + 1, i, -1)


def draw(stdscr):
    config = load_config()

    curses.curs_set(0)
    stdscr.nodelay(True)
    init_colors()

    hue_offset = 0
    last_update = 0
    player_data = ("Stopped", "No Track", "", 0, 1)

    while True:
        now = time.time()

        # --- реже обновляем playerctl
        if now - last_update > 0.5:
            player_data = get_player_info()
            last_update = now

        status, title, artist, pos, length = player_data

        stdscr.erase()
        height, width = stdscr.getmaxyx()
        bar_width = width - 4

        # --- заголовок
        text = f"♪ {title} - {artist}"
        stdscr.addstr(1, max(0, (width - len(text)) // 2), text[:width-1])

        # --- визуализатор
        for i in range(bar_width):
            if status == "Playing":
                char = random.choice("▁▂▃▄▅▆▇█")
            else:
                char = "─"

            if config.get("rgb", False):
                hue = (i / max(bar_width, 1) + hue_offset) % 1.0
                r, g, b = colorsys.hsv_to_rgb(hue, 1, 1)

                color_id = int(hue * 254) + 1

                try:
                    curses.init_color(
                        color_id,
                        int(r * 1000),
                        int(g * 1000),
                        int(b * 1000)
                    )
                    curses.init_pair(color_id, color_id, -1)
                    color = curses.color_pair(color_id)
                except:
                    color = curses.color_pair(1)

            elif config.get("single_color", False):
                c = color_map.get(config.get("player_color", "cyan"), curses.COLOR_CYAN)
                color = curses.color_pair(c + 1)

            else:
                color = curses.color_pair(1)

            try:
                stdscr.addstr(3, 2 + i, char, color)
            except:
                pass

        # --- прогресс бар
        ratio = pos / length if length > 0 else 0
        filled = int(bar_width * ratio)
        bar = "█" * filled + "─" * (bar_width - filled)

        try:
            stdscr.addstr(5, 2, bar[:bar_width])
        except:
            pass

        # --- время 00:00
        time_str = f"{status} ▶ {format_time(pos)} / {format_time(length)}"
        try:
            stdscr.addstr(7, max(0, (width - len(time_str)) // 2), time_str[:width-1])
        except:
            pass

        stdscr.refresh()
        time.sleep(0.05)

        hue_offset += 0.01

        if stdscr.getch() == ord('q'):
            break


if __name__ == "__main__":
    curses.wrapper(draw)
