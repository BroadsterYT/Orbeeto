#pragma once

#include <vector>
#include "Component.hpp"
#include "../TextureManager.hpp"
#include "../Game.hpp"


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
	std::string spritePath = "Assets/orbeeto.png";
	std::shared_ptr<SDL_Texture> spriteSheet = nullptr;


	void serialize(std::ofstream& out) {
		SerialHelper::serialize(out, &layer, &tileWidth, &tileHeight, 
			&posX, &posY, &angle, &moveWithRoom,
			&srcRect, &destRect,
			&ignoreScaling, &index, &spritePath
		);
	}

	void deserialize(std::ifstream& in) {
		SerialHelper::deserialize(in, &layer, &tileWidth, &tileHeight,
			&posX, &posY, &angle, &moveWithRoom,
			&srcRect, &destRect,
			&ignoreScaling, &index, &spritePath
		);

		//spriteSheet = TextureManager::loadTexture(Game::renderer, spritePath);
	}
};