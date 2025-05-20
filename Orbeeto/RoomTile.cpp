#include "RoomTile.hpp"
#include <cassert>
#include <stdexcept>


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
	SDL_Texture* tileSheet = nullptr;  // The original image file to extract all needed tiles from
	SDL_Texture* finalImage = SDL_CreateTexture(Game::renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, finalWidth, finalHeight);  // The final image/spritesheet to use for the tile's sprite

	SDL_Rect srcRect = { 0, 0, tileSize, tileSize };
	SDL_Rect destRect = { 0, 0, tileSize, tileSize };

	switch (tileSet) {  // Selecting a tile sheet
	case 0:
		tileSheet = TextureManager::loadTexture(Game::renderer, "Assets/tile1.png");
		
		// Don't need to destroy/reassign finalImage; uses default
		SDL_SetTextureBlendMode(finalImage, SDL_BLENDMODE_BLEND);
		SDL_SetRenderTarget(Game::renderer, finalImage);

		srcRect.y = tileSize * subset;

		noAnimTilingScheme1(style, tileSize, tileSheet, srcRect, destRect);
		break;

	default:
		throw std::invalid_argument("Error: \"tileSet\" must be a valid input.");
	}
	SDL_SetRenderTarget(Game::renderer, NULL);
	SDL_DestroyTexture(tileSheet);

	// ----- Assigning components ----- //

	Game::ecs.assignComponent<Transform>(Game::stack.peek(), tile);
	Transform* transform = Game::ecs.getComponent<Transform>(Game::stack.peek(), tile);
	transform->pos = Vector2(tileSize * posX + finalWidth / 2, tileSize * posY + finalHeight / 2);

	if (!invisible) {
		Game::ecs.assignComponent<Sprite>(Game::stack.peek(), tile);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), tile);
		*sprite = Sprite(0, 0, finalWidth, finalHeight);
		sprite->spriteSheet = finalImage;
	}

	if (solid) {
		Game::ecs.assignComponent<Collision>(Game::stack.peek(), tile);
		Collision* coll = Game::ecs.getComponent<Collision>(Game::stack.peek(), tile);
		coll->hitWidth = finalWidth;
		coll->hitHeight = finalHeight;

		coll->physicsTags.set(PTags::WALL);
		coll->physicsTags.set(PTags::CAN_PUSH);
		if (canHoldPortal) {
			coll->physicsTags.set(PTags::CAN_HOLD_PORTAL);
		}
	}

	return tile;
}

void RoomTile::setSolid(bool isSolid) {
	solid = isSolid;
}

void RoomTile::setInvisibility(bool isInvis) {
	invisible = isInvis;
}

void RoomTile::setCanHoldPortal(bool canHold) {
	canHoldPortal = canHold;
}

void RoomTile::noAnimTilingScheme1(int style, int tileSize, SDL_Texture* tileSheet, SDL_Rect& srcRect, SDL_Rect& destRect) {
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
	{
		for (int y = 0; y < height; y++) {
			for (int x = 0; x < width; x++) {
				double angle = 0.0;

				if (y == 0 && x == 0) {  // Northwest corner
					srcRect.x = tileSize * 2;
					angle = 180.0;
				}
				else if (y == 0 && x == width - 1) {  // Northeast
					srcRect.x = tileSize * 2;
					angle = 270.0;
				}
				else if (y == height - 1 && x == 0) {  // Southwest
					srcRect.x = tileSize * 2;
					angle = 90.0;
				}
				else if (y == height - 1 && x == width - 1) {  // Southeast
					srcRect.x = tileSize * 2;
				}
				else if (y == height - 1) {  // Southern border
					srcRect.x = tileSize * 1;
				}
				else if (x == width - 1) {  // Eastern border
					srcRect.x = tileSize * 1;
					angle = 270.0;
				}
				else if (y == 0) {  // Northern border
					srcRect.x = tileSize * 1;
					angle = 180.0;
				}
				else if (x == 0) {  // Western border
					srcRect.x = tileSize * 1;
					angle = 90.0;
				}

				// Single tile thick
				if (x == 0 && height == 1) {
					srcRect.x = tileSize * 3;
					angle = 90.0;
				}
				else if (x == width - 1 && height == 1) {
					srcRect.x = tileSize * 3;
					angle = 270.0;
				}
				else if (y == 0 && width == 1) {
					srcRect.x = tileSize * 3;
					angle = 180.0;
				}
				else if (y == height - 1 && width == 1) {
					srcRect.x = tileSize * 3;
					angle = 0.0;
				}
				else if (height == 1) {
					srcRect.x = tileSize * 4;
					angle = 90.0;
				}
				else if (width == 1) {
					srcRect.x = tileSize * 4;
					angle = 0.0;
				}

				// Single block
				if (width == 1 && height == 1) {
					srcRect.x = tileSize * 5;
					angle = 0.0;
				}

				destRect.x = x * tileSize;
				destRect.y = y * tileSize;
				SDL_RenderCopyEx(Game::renderer, tileSheet, &srcRect, &destRect, angle, NULL, SDL_FLIP_NONE);
				srcRect.x = 0;
			}
		}
	}
		break;

	default:
		break;
	}
}