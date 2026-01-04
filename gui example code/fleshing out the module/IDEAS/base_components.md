# UI Widgets Documentation

## Widget (Root)
**Purpose:** Fundamental building block for all UI elements.  
Provides geometry, hierarchy, visibility, and update/draw control.  

### Key Attributes
- `pos: V2` → Widget’s center position.  
- `size: V2` → Widget’s width & height.  
- `padding: V4` → Space inside widget boundary `[left, top, right, bottom]`.  
- `margin: V4` → Space outside widget boundary `[left, top, right, bottom]`.  
- `children: list[Widget]` → Optional child widgets (for recursive updates/draws).  
- `parent: Widget | None` → Parent widget reference.  
- `visible: bool` → Whether the widget should be drawn.  
- `enabled: bool` → Whether the widget can interact with events.  
- `is_dirty: bool` → Flag indicating widget needs update/redraw.  
- `is_child: bool` → Whether this widget is a child (affects recursive update/draw).  
- `flex_grow: int` → CSS's Flex Grow.  


---
## Container
**Purpose:** Layout and organize children widgets.

### Types
- **Row**: Horizontally arranges children.  
- **Col**: Vertically arranges children.  
- **Div**: Generic container for arbitrary grouping with no strict layout.  
- **Grid**: Arranges children in a 2D grid with rows and columns.  

### Key Parameters
- `grid_size` (V2: for grid, row, col)  
- `spacing` (V2: for grid, row, col)  
- `alignment` (start, center, end)  

### Alignments Options for Both Axes
- `start` — Align items to the start (left/top) of the container.  
- `center` — Align items centered in the container.  
- `end` — Align items to the end (right/bottom) of the container.  
- `stretch` — Expand items to fill the available space.  
- `space-between` — Distribute items evenly, first at start and last at end.  
- `space-around` — Distribute items evenly with equal space around each item.  
- `space-evenly` — Distribute items with equal space between all items and container edge  

---

## Static
**Purpose:** Display-only, non-interactive visuals.

### Types
- **Canvas**: Blank drawable surface for custom rendering.  
- **Image**: Shows image content from source.  
- **Video**: Embeds video playback.  

---

## Interactive
**Purpose:** User input and interactive elements.

### Types
- **Button**: Clickable button.  
- **Slider**: Adjustable value slider.  
- **Toggle**: Switch or checkbox.  
- **Text**: Editable single-line text input.  
- **Input Field**: Editable multi-line text input.  
- **Paragraph Field**: Larger multi-line text blocks.  
- **Menus**: Dropdown or popup menus.  

### Key Parameters
- `hovered`, `pressed`, `focused` states (bool)  
- `event callbacks` (`on_click`, `on_hover`, `on_keydown`, etc.)  
- `value/state` storage depending on widget  

---

## Future Extras
Examples of potential extended UI features:
- Tables  
- Joysticks  
- Vector graphics  
- Animations  

