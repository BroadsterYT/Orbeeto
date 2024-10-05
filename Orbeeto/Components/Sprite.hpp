#pragma once
#include "../TextureManager.hpp"


struct Sprite {
	SDL_Renderer* renderer;
	const char* fileLocation;

	int tileWidth;
	int tileHeight;
	int posX;
	int posY;

	double angle = 0;

	bool moveWithRoom = true;

	int tilePosX = 0;
	int tilePosY = 0;

	SDL_Rect srcRect = {tilePosX, tilePosY, tileWidth, tileHeight};
	SDL_Rect destRect = {posX, posY, tileWidth, tileHeight};

	SDL_Texture* image = TextureManager::loadTexture(renderer, "assets/orbeeto.png");
};