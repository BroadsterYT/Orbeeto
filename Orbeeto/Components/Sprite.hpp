#pragma once
#include "../TextureManager.hpp"

/// <summary>
/// Draws an image onto the screen
/// </summary>
/// <param name="renderer">The renderer to draw the image</param>
/// <param name="fileLocation">The file location of the sprite sheet</param>
/// <param name="tileWidth">The width of each individual sprite in the sprite sheet</param>
/// <param name="tileHeight">The height of each individual sprite in the sprite sheet</param>
/// <param name="posX">The x-position on the screen to draw the sprite</param>
/// <param name="posY">The y-position on the screen to draw the sprite</param>
/// <param name="angle">The angle to rotate the sprite before drawing. Defualts to 0.</param>
/// <param name="moveWithRoom">Should this sprite be affected by the room/camera? Defaults to true.</param>
/// <param name="tilePosX">The x-position on the sprite sheet to "snip" a sprite from. Defaults to 0.</param>
/// <param name="tilePosY">The y-position on the sprite sheet to "snip" a sprite from. Defaults to 0.</param>
struct Sprite {
	SDL_Renderer* renderer;
	const char* fileLocation;

	int tileWidth;
	int tileHeight;
	int posX;
	int posY;

	double angle = 0;  // The angle the texture should be rotated to

	bool moveWithRoom = true;  // Does this sprite move with the room?

	int tilePosX = 0;
	int tilePosY = 0;

	SDL_Rect srcRect = {tilePosX, tilePosY, tileWidth, tileHeight};
	SDL_Rect destRect = {posX, posY, tileWidth, tileHeight};

	SDL_Texture* image = nullptr;
};