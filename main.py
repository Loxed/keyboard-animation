from manim import *
import json
import random

class Keyboard(Scene):
    def construct(self):
        # Load configuration from the JSON file
        try:
            # It's good practice to specify encoding, especially with special characters
            with open("keyboard_config.json", "r", encoding="utf-8") as f:
                config = json.load(f)
        except FileNotFoundError:
            self.add(Text("Error: keyboard_config.json not found.", color=RED))
            return
        except json.JSONDecodeError:
            self.add(Text("Error: Could not decode keyboard_config.json.", color=RED))
            return

        # Set a pure black background
        self.camera.background_color = BLACK

        # Get the selected layout from config
        selected_layout = config.get("selected_layout", "qwerty_us")
        if "layouts" in config and selected_layout in config["layouts"]:
            layout = config["layouts"][selected_layout]
        else:
            # Fallback to first layout if selected layout is not found
            layout = list(config["layouts"].values())[0] if "layouts" in config else []
            
        # Create the keyboard using the selected layout and categories
        keyboard = self.create_keyboard(layout, config["categories"])
        self.add(keyboard)  # Display keyboard instantly
        self.wait(1)

        # "Click" and expand the keys for the video topic defined in the JSON
        self.click_and_expand(keyboard, config)

        self.wait(2)

    def get_key_width(self, key_str):
        """Returns the width for specific keys based on a standard US QWERTY layout."""
        if key_str == "Space":
            return 6.0
        if key_str == "Enter":
            return 2.5
        if key_str in ["Shift", "Caps Lock"]:
            return 2.2
        if key_str == "Tab":
            return 1.5
        if key_str in ["Control", "Option", "Alt", "Alt Gr"]:
            return 1.2
        return 1.0  # Standard key width

    def create_keyboard(self, layout, categories):
        """Creates the visual representation of the keyboard with retro styling."""
        keyboard = VGroup()
        self.keys = {}
        self.key_positions = {}  # Track positions for proper identification

        key_height = 1.0
        key_spacing = 0.12
        y_pos = 3.5  # Starting y-position

        for row_idx, row in enumerate(layout):
            # Calculate the width of the row for centering
            total_row_width = sum([self.get_key_width(key) for key in row]) + (len(row) - 1) * key_spacing
            x_pos = -total_row_width / 2

            for col_idx, key_str in enumerate(row):
                key_width = self.get_key_width(key_str)
                is_alpha = key_str in categories and len(key_str) == 1

                # Retro keyboard styling with gradient-like effect
                if is_alpha:
                    key_color = "#4A4A4A"  # Medium gray for alpha keys
                    stroke_color = "#6A6A6A"
                else:
                    key_color = "#2A2A2A"  # Darker for function keys
                    stroke_color = "#4A4A4A"
                
                key = RoundedRectangle(
                    corner_radius=0.08,  # Smaller radius for more retro look
                    width=key_width, 
                    height=key_height,
                    fill_color=key_color, 
                    fill_opacity=1.0, 
                    stroke_color=stroke_color, 
                    stroke_width=2
                )
                
                # Add a subtle inner highlight for 3D effect
                inner_highlight = RoundedRectangle(
                    corner_radius=0.06,
                    width=key_width - 0.1,
                    height=key_height - 0.1,
                    fill_color=WHITE,
                    fill_opacity=0.1,
                    stroke_width=0
                )
                
                key.move_to(RIGHT * (x_pos + key_width / 2) + UP * y_pos)
                inner_highlight.move_to(key.get_center() + UP * 0.05)  # Slight offset for 3D effect
                
                # Retro font styling
                text_size = 18 if len(key_str) > 2 else 24
                letter_text = Text(
                    key_str, 
                    font_size=text_size, 
                    weight=BOLD,
                    font="monospace"  # Monospace for retro feel
                ).move_to(key.get_center())
                letter_text.set_color("#E0E0E0")  # Light gray text
                
                key_group = VGroup(key, inner_highlight, letter_text)
                
                # Use unique identifier for duplicate keys
                key_id = f"{key_str}_{row_idx}_{col_idx}"
                self.keys[key_id] = key_group
                self.key_positions[key_str] = self.key_positions.get(key_str, []) + [key_id]
                
                keyboard.add(key_group)

                x_pos += key_width + key_spacing

            y_pos -= key_height + key_spacing

        keyboard.scale(0.8).move_to(ORIGIN)
        return keyboard

    def play_typing_sound(self, sound_file):
        """Play typing sound if file is provided and exists."""
        if sound_file:
            try:
                # Note: Manim doesn't have built-in sound support during rendering
                # This is a placeholder for sound functionality
                # In practice, you'd add sound in post-processing or use external tools
                pass
            except:
                pass

    def click_and_expand(self, keyboard, config):
        """Highlights specified keys and shows a combined content card."""
        topic_info = config["video_topic"]
        topic_keys = topic_info["keys"]
        topic_title = topic_info["title"]
        topic_sections = topic_info.get("sections", {})
        categories = config["categories"]
        
        # Get animation settings from config
        animation_config = config.get("animation", {})
        typing_speed = animation_config.get("typing_speed", 0.2)
        highlight_color = animation_config.get("highlight_color", "#00FF88")
        randomness = animation_config.get("randomness", 0.1)
        sound_file = animation_config.get("sound_file", None)
        
        # Sequential "click" animation with highlight effect and randomness
        selected_key_ids = []
        keys_to_animate = topic_keys.copy()
        
        if randomness > 0:
            # Add random delay variation
            random.shuffle(keys_to_animate)
        
        for key in keys_to_animate:
            if key in self.key_positions:
                # Use the first occurrence of the key
                key_id = self.key_positions[key][0]
                selected_key_ids.append(key_id)
                
                # Play sound effect
                self.play_typing_sound(sound_file)
                
                # Highlight the key with a glow effect
                glow = self.keys[key_id][0].copy()  # Copy the main rectangle
                glow.set_fill(color=highlight_color, opacity=0.3)
                glow.set_stroke(color=highlight_color, width=3)
                
                self.play(
                    self.keys[key_id].animate.scale(0.95),
                    FadeIn(glow),
                    run_time=0.15,
                    rate_func=there_and_back
                )
                
                # Add the glow to the key group permanently
                self.keys[key_id].add(glow)
                
                # Add random delay if randomness is enabled
                if randomness > 0:
                    random_delay = random.uniform(0, randomness)
                    self.wait(typing_speed + random_delay)
                else:
                    self.wait(typing_speed)

        # Group selected and unselected keys
        selected_key_mobjects = VGroup(*[self.keys[k] for k in selected_key_ids])
        
        # Create list of all unselected key IDs
        all_key_ids = list(self.keys.keys())
        unselected_key_ids = [k for k in all_key_ids if k not in selected_key_ids]
        unselected_keys = VGroup(*[self.keys[k] for k in unselected_key_ids])
        
        # Hide unselected keys smoothly and bring selected keys to front immediately
        self.play(FadeOut(unselected_keys, scale=0.8), run_time=0.8)
        self.bring_to_front(selected_key_mobjects)
        
        # Create the retro-styled info card
        expanded_width, expanded_height = 12, 8
        expanded_card = RoundedRectangle(
            corner_radius=0.2, 
            width=expanded_width, 
            height=expanded_height,
            fill_color="#1A1A2E", 
            fill_opacity=0.95, 
            stroke_color=highlight_color, 
            stroke_width=3
        )
        
        # Add inner border for retro CRT monitor effect
        inner_border = RoundedRectangle(
            corner_radius=0.15,
            width=expanded_width - 0.3,
            height=expanded_height - 0.3,
            fill_color="#1A1A2E",
            stroke_color="#004A2F",
            stroke_width=2
        )
        
        # Group the card backgrounds and send to back immediately
        card_group = VGroup(expanded_card, inner_border)
        self.bring_to_back(card_group)
        
        # Retro-styled title
        title = Text(
            topic_title, 
            font_size=44, 
            weight=BOLD,
            font="monospace",
            color=highlight_color
        )
        title.move_to(expanded_card.get_top() + DOWN * 0.8)
        
        # Create content sections with proper line wrapping
        content_sections = VGroup()
        max_width = expanded_width - 2  # Leave margin
        
        for key in topic_keys:
            if key in categories and key in topic_sections:
                category_text = categories[key]
                section_detail = topic_sections[key]
                full_text = f"• {category_text}: {section_detail}"
                
                # Create text and check if it needs wrapping
                section_mobject = Text(
                    full_text, 
                    font_size=20, 
                    weight=NORMAL,
                    font="monospace",
                    color="#B0FFD1"
                )
                
                # If text is too wide, wrap it
                if section_mobject.width > max_width:
                    # Split into category and detail for better wrapping
                    category_line = Text(
                        f"• {category_text}:",
                        font_size=20,
                        weight=BOLD,
                        font="monospace",
                        color="#B0FFD1"
                    )
                    detail_line = Text(
                        f"  {section_detail}",
                        font_size=18,
                        weight=NORMAL,
                        font="monospace",
                        color="#90E0B1"
                    )
                    
                    wrapped_section = VGroup(category_line, detail_line)
                    wrapped_section.arrange(DOWN, buff=0.1, aligned_edge=LEFT)
                    content_sections.add(wrapped_section)
                else:
                    content_sections.add(section_mobject)
                
        content_sections.arrange(DOWN, buff=0.4, aligned_edge=LEFT)
        content_sections.next_to(title, DOWN, buff=0.8)
        
        # Group all content (card is already grouped and sent to back)
        info_card = VGroup(card_group, title, content_sections)
        info_card.move_to(ORIGIN)
        
        # Position selected keys at the bottom of the viewport
        frame_height = self.camera.frame_height
        target_keys_layout = selected_key_mobjects.copy()
        target_keys_layout.arrange(RIGHT, buff=0.4)
        
        # Position keys near the bottom of the viewport
        bottom_y_position = -frame_height/2 + 1.5  # 1.5 units from bottom
        target_keys_layout.move_to(DOWN * abs(bottom_y_position))
        
        # Ensure keys don't exceed viewport width
        frame_width = self.camera.frame_width
        if target_keys_layout.width > frame_width - 2:
            target_keys_layout.scale((frame_width - 2) / target_keys_layout.width)

        # Smooth animation: card appears while keys move to bottom
        self.play(
            FadeIn(card_group, shift=UP * 0.3, scale=0.9),
            FadeIn(title, shift=UP * 0.3),
            selected_key_mobjects.animate.become(target_keys_layout),
            run_time=1.5,
            rate_func=smooth
        )
        
        # Keep keys in front throughout
        self.bring_to_front(selected_key_mobjects)
        
        # Type out the content sections progressively
        self.type_content_progressively(content_sections, typing_speed * 2)
        self.wait(3)

        # Final fade out with retro effect
        all_content = VGroup(card_group, title, content_sections, selected_key_mobjects)
        self.play(
            FadeOut(all_content, shift=DOWN * 0.2, scale=1.1), 
            run_time=0.8,
            rate_func=smooth
        )

    def type_content_progressively(self, content_sections, typing_delay):
        """Type out content sections with a typewriter effect."""
        for section in content_sections:
            if isinstance(section, VGroup):  # Wrapped text (category + detail)
                for subsection in section:
                    self.play(FadeIn(subsection, shift=RIGHT * 0.1), run_time=typing_delay)
                    self.wait(typing_delay * 0.5)
            else:  # Single line text
                self.play(FadeIn(section, shift=RIGHT * 0.1), run_time=typing_delay)
                self.wait(typing_delay * 0.5)