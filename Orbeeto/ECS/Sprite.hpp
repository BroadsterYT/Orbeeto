#pragma once
#include "../TextureManager.hpp"

/// <summary>
/// A sprite component that allows an entity to draw an image onto the screen
/// </summary>
/// <param name = 'renderer'> The renderer to use </param>
/// <param name = 'fileLocation'> The path to the image to display </param>
/// <param name = 'tileWidth'> The width of each image </param>
/// <param name = 'tileHeight'> The height of each image </param>
/// <param name = 'posX'> The x-axis posiiton to draw the image </param>
/// <param name = 'posY'> The y-axis posiiton to draw the image </param>
/// <param name = 'srcRect'> The source rectangle to take the snip from </param>
/// <param name = 'destRect'> The destination rectangle to draw the snip onto </param>
struct Sprite {
	SDL_Renderer* renderer;
	const char* fileLocation;

	int tileWidth;
	int tileHeight;
	int posX;
	int posY;

	SDL_Rect srcRect = {0, 0, tileWidth, tileHeight};
	SDL_Rect destRect = {posX, posY, tileWidth, tileHeight};

	SDL_Texture* image = TextureManager::loadTexture(renderer, "assets/orbeeto.png");
};