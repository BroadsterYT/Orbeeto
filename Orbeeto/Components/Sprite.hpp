#pragma once
#include "../TextureManager.hpp"


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

	SDL_Texture* image = TextureManager::loadTexture(renderer, "assets/orbeeto.png");
};