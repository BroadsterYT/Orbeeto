#pragma once
#include <vector>
#include "Component.hpp"
#include "../TextureManager.hpp"

/// <summary>
/// Draws an image onto the screen
/// </summary>
/// <param name="tileWidth">The width of each individual sprite in the sprite sheet</param>
/// <param name="tileHeight">The height of each individual sprite in the sprite sheet</param>
/// <param name="posX">The x-position on the screen to draw the sprite</param>
/// <param name="posY">The y-position on the screen to draw the sprite</param>
/// <param name="angle">The angle to rotate the sprite before drawing. Defualts to 0.</param>
/// <param name="moveWithRoom">Should this sprite be affected by the room/camera? Defaults to true.</param>
struct Sprite : Component {
	int tileWidth;
	int tileHeight;
	int posX;
	int posY;
	double angle = 0;  // The angle the texture should be rotated to
	bool moveWithRoom = true;  // Does this sprite move with the room?

	SDL_Rect srcRect = {0, 0, tileWidth, tileHeight};
	SDL_Rect destRect = {posX, posY, tileWidth, tileHeight};

	int index = 0;  // The index of the image in the image vector to display
	SDL_Texture* spriteSheet = nullptr;

	/// <summary>
	/// Places the source rectangle at the desired sprite in the spritesheet
	/// </summary>
	/// <param name="spritesPerRow">The number of sprites per row in the sprite sheet</param>
	void setSpriteFromIndex(int spritesPerRow) {
		int finalX = 0;
		int finalY = 0;

		for (int i = 0; i < index; i++) {
			if ((i + 1) % spritesPerRow == 0) {
				finalX = 0;
				finalY += tileHeight;
			}
			else {
				finalX += tileWidth;
			}
		}

		srcRect.x = finalX;
		srcRect.y = finalY;
	}
};