# Alphabet Grid Animation

This is a ManimCE animation that creates a 5x6 grid of letter tiles (A to Z), where each tile shows a letter and its corresponding category. After displaying the full grid for a few seconds, it zooms into a selected tile, which then expands to show more details about that category.

## Features

- 5x6 grid of letter tiles (A to Z)
- Each tile shows a letter and its corresponding category
- Smooth animation that zooms into a selected tile
- Detailed view shows the full category title and content ideas
- Customizable categories and content ideas via JSON files
- Modular design for easy letter selection

## Usage

### Basic Usage

To run the basic animation that zooms into the "C" tile:

```bash
manim -p alphabet_grid/main.py AlphabetGrid
```

### Modular Usage

To run the modular version that allows selecting different letters:

```bash
manim -p alphabet_grid_modular.py AlphabetGridA  # Zoom into A
manim -p alphabet_grid_modular.py AlphabetGridB  # Zoom into B
manim -p alphabet_grid_modular.py AlphabetGridC  # Zoom into C
```

### Using the Run Script

For convenience, you can use the provided run script to select a letter:

```bash
python run_animation.py A  # Zoom into A
python run_animation.py B  # Zoom into B
python run_animation.py C  # Zoom into C
```

If no letter is provided, it defaults to "C".

### Customization

You can customize the categories and content ideas by creating JSON files:

1. Copy the example files:
   ```bash
   cp alphabet_grid/categories.json.example alphabet_grid/categories.json
   cp alphabet_grid/content_ideas.json.example alphabet_grid/content_ideas.json
   ```

2. Edit the JSON files to customize the categories and content ideas.

3. Run the animation as usual.

## Structure

- `main.py`: Basic implementation of the alphabet grid animation
- `alphabet_grid_modular.py`: Modular implementation with more features
- `categories.json.example`: Example file for customizing categories
- `content_ideas.json.example`: Example file for customizing content ideas
- `manim.cfg`: Configuration file for ManimCE

## Requirements

- ManimCE (Community Edition)
- Python 3.7+