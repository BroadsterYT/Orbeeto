#include "SpriteSystem.hpp"
#include "../Components/AccelTransform.hpp"
#include "../Components/Sprite.hpp"
#include "../Rooms/Room.hpp"


void SpriteSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void SpriteSystem::render(SDL_Renderer* renderer) {
	for (const auto& entity : mEntities) {
		auto& sprite = coordinator->getComponent<Sprite>(entity);
		auto& accelTransform = coordinator->getComponent<AccelTransform>(entity);

		if (sprite.moveWithRoom) {
			sprite.destRect.x = accelTransform.pos.x - sprite.tileWidth / 2 - Room::camera.getX();
			sprite.destRect.y = accelTransform.pos.y - sprite.tileHeight / 2 - Room::camera.getY();
		}
		else {
			sprite.destRect.x = accelTransform.pos.x - sprite.tileWidth / 2;
			sprite.destRect.y = accelTransform.pos.y - sprite.tileHeight / 2;
		}

		sprite.image = TextureManager::loadTexture(Game::renderer, sprite.fileLocation);

		SDL_RenderCopyEx(sprite.renderer, sprite.image, &sprite.srcRect, &sprite.destRect, sprite.angle, NULL, SDL_FLIP_NONE);
	}
}