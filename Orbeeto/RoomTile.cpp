#include "RoomTile.hpp"
#include <cassert>
#include "Game.hpp"


RoomTile::RoomTile(int posX = 0, int posY = 0, int width = 4, int height = 4,
	int tileSet = 0, int subset = 0, int style = 0) {
	this->posX = posX;
	this->posY = posY;
	this->width = width;
	this->height = height;

	this->tileSet = tileSet;
	this->subset = subset;
	this->style = style;
}

Entity RoomTile::buildTile() {
	assert(width >= 0 && height >= 0 && "Tile must have positive, non-zero dimensions.");
	Entity tile = Game::ecs.createEntity(Game::stack.peek());

	int tileSize = 16;  // The size of each individual tile
	int finalWidth = tileSize * width;
	int finalHeight = tileSize * height;
	SDL_Texture* tileSheet = TextureManager::loadTexture(Game::renderer, "Assets/wall.png");

	switch (tileSet) {  // Selecting a tile sheet
	case 0:
		break;
	default:
		break;
	}

	SDL_Texture* finalImage = SDL_CreateTexture(Game::renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, finalWidth, finalHeight);
	SDL_SetTextureBlendMode(finalImage, SDL_BLENDMODE_BLEND);
	SDL_SetRenderTarget(Game::renderer, finalImage);

	SDL_Rect srcRect = { 0, 0, tileSize, tileSize };
	SDL_Rect destRect = { 0, 0, tileSize, tileSize };

	// Selecting tile subset
	srcRect.y = tileSize * subset;

	switch (style) {
	case 0:  // Standard tiling, tesselate image with first tile
		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				destRect.x = x * tileSize;
				destRect.y = y * tileSize;
				SDL_RenderCopy(Game::renderer, tileSheet, &srcRect, &destRect);
			}
		}
		break;

	case 1:  // Full bordering
		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				if (y == 0 && x == 0) {  // Northwest corner
					srcRect.x = tileSize * 7;
				}
				else if (y == 0 && x == width - 1) {  // Northeast
					srcRect.x = tileSize * 6;
				}
				else if (y == height - 1 && x == 0) {  // Southwest
					srcRect.x = tileSize * 8;
				}
				else if (y == height - 1 && x == width - 1) {  // Southeast
					srcRect.x = tileSize * 5;
				}
				else if (y == height - 1) {  // Southern border
					srcRect.x = tileSize * 1;
				}
				else if (x == width - 1) {  // Eastern border
					srcRect.x = tileSize * 2;
				}
				else if (y == 0) {  // Northern border
					srcRect.x = tileSize * 3;
				}
				else if (x == 0) {  // Western border
					srcRect.x = tileSize * 4;
				}

				destRect.x = x * tileSize;
				destRect.y = y * tileSize;
				SDL_RenderCopy(Game::renderer, tileSheet, &srcRect, &destRect);
				srcRect.x = 0;
			}
		}
		break;

	default:
		break;
	}
	SDL_SetRenderTarget(Game::renderer, NULL);
	SDL_DestroyTexture(tileSheet);

	// ----- Assigning components ----- //

	return tile;
}

void RoomTile::setSolid(bool isSolid) {
	solid = isSolid;
}

void RoomTile::setInvisibility(bool isInvis) {
	invisible = isInvis;
}