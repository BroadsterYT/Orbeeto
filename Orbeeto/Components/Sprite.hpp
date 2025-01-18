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
	int layer = 0;
	bool isRendered = false;
	int tileWidth = 64;
	int tileHeight = 64;
	int posX = 0;
	int posY = 0;
	double angle = 0;  // The angle the texture should be rotated to
	bool moveWithRoom = true;  // Does this sprite move with the room?

	SDL_Rect srcRect = {0, 0, tileWidth, tileHeight};
	SDL_Rect destRect = {posX, posY, tileWidth, tileHeight};

	int index = 0;  // The index of the image in the image vector to display
	SDL_Texture* spriteSheet = nullptr;
};