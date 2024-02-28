# Tile Sprite Arrangement

## Description
Tile sprite sheets have a setup that is necessary for the game to display them properly. The setup rules are described
below:
1. The animation sequence of the sprite sheet is laid out along the x-axis (from left to right)
2. Each tile is placed on its own line along the y-axis (from top to bottom)
3. Every tile must have the same number of animation frames in a sprite sheet.

## Example

| Tile |      Frame 1       |      Frame 2       |       Frame 3       |       Frame 4       |       Frame 5       |       Frame 6       |       Frame 7       |       Frame 8       | ... |
|:-----|:------------------:|:------------------:|:-------------------:|:-------------------:|:-------------------:|:-------------------:|:-------------------:|:-------------------:|-----|
| 1    | Tile 1<br/>Frame 1 | Tile 1<br/>Frame 2 | Tile 1 <br/>Frame 3 | Tile 1 <br/>Frame 4 | Tile 1 <br/>Frame 5 | Tile 1 <br/>Frame 6 | Tile 1 <br/>Frame 7 | Tile 1 <br/>Frame 8 | ... |
| 2    | Tile 2<br/>Frame 1 | Tile 2<br/>Frame 2 | Tile 2 <br/>Frame 3 | Tile 2 <br/>Frame 4 | Tile 2 <br/>Frame 5 | Tile 2 <br/>Frame 6 | Tile 2 <br/>Frame 7 | Tile 2 <br/>Frame 8 | ... |
| 3    | Tile 3<br/>Frame 1 | Tile 3<br/>Frame 2 | Tile 3 <br/>Frame 3 | Tile 3 <br/>Frame 4 | Tile 3 <br/>Frame 5 | Tile 3 <br/>Frame 6 | Tile 3 <br/>Frame 7 | Tile 3 <br/>Frame 8 | ... |
| ...  |        ...         |        ...         |         ...         |         ...         |         ...         |         ...         |         ...         |         ...         | ... |
