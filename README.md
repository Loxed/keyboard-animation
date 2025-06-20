# Keyboard Animation

This is a ManimCE animation that creates a keyboard layout visualization. The animation highlights specific keys and displays information related to those keys. The keyboard layout is customizable through a JSON configuration file.

## Features

- Multiple keyboard layouts (QWERTY US, QWERTY UK, BEPO, Alphabetical, Experimental)
- Customizable keyboard layout selection via JSON configuration
- Animated key highlighting and expansion
- Detailed information cards for selected keys
- Customizable categories and topics via JSON configuration
- Smooth animations with configurable timing and effects

## Usage

### Basic Usage

To run the animation:

```bash
manim -p main.py Keyboard
```

### Customization

You can customize the keyboard layout and other settings by editing the `keyboard_config.json` file:

1. Select a keyboard layout by changing the `selected_layout` value:
   ```json
   "selected_layout": "qwerty_us"
   ```

2. Available layouts:
   - `qwerty_us`: Standard US QWERTY layout
   - `qwerty_uk`: UK QWERTY layout
   - `bepo`: BÉPO French layout
   - `alphabetical`: Keys arranged in alphabetical order
   - `experimental`: Experimental layout based on letter frequency

3. Customize categories, topics, and animation settings in the same JSON file.

## Configuration

The `keyboard_config.json` file contains the following sections:

- `selected_layout`: The keyboard layout to use
- `layouts`: Definitions of different keyboard layouts
- `categories`: Category definitions for each letter key
- `video_topic`: Information about the topic to highlight
- `animation`: Animation settings like speed and colors

## Requirements

- ManimCE (Community Edition)
- Python 3.7+