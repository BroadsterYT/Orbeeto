#pragma once

#include <vector>
#include "Component.hpp"
#include "../TextureManager.hpp"


struct Sprite : Component {
	Sprite(int x = 0, int y = 0, int w = 64, int h = 64) {
		posX = x;
		posY = y;
		tileWidth = w;
		tileHeight = h;

		srcRect = { 0, 0, w, h };
		destRect = { x, y, w, h };
	}
	
	int layer = 0;

	int tileWidth = 64;
	int tileHeight = 64;
	int posX = 0;
	int posY = 0;
	double angle = 0;  // The angle the texture should be rotated to
	bool moveWithRoom = true;  // Does this sprite move with the room?

	SDL_Rect srcRect = { 0, 0, tileWidth, tileHeight };
	SDL_Rect destRect = { posX, posY, tileWidth, tileHeight };

	bool ignoreScaling = false; // Should this sprite ignore the scalaing of the viewport?

	int index = 0;  // The index of the image in the image vector to display
	SDL_Texture* spriteSheet = nullptr;
};