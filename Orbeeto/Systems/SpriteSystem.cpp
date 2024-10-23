#include "SpriteSystem.hpp"
#include "../Components/Transform.hpp"
#include "../Rooms/Room.hpp"
#include <iostream>


void SpriteSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void SpriteSystem::render(SDL_Renderer* renderer) {
	for (const auto& entity : mEntities) {
		auto& sprite = coordinator->getComponent<Sprite>(entity);
		auto& transform = coordinator->getComponent<Transform>(entity);

		if (sprite.moveWithRoom) {
			sprite.destRect.x = transform.pos.x - sprite.tileWidth / 2 - Room::camera.getX();
			sprite.destRect.y = transform.pos.y - sprite.tileHeight / 2 - Room::camera.getY();
		}
		else {
			sprite.destRect.x = transform.pos.x - sprite.tileWidth / 2;
			sprite.destRect.y = transform.pos.y - sprite.tileHeight / 2;
		}

		std::cout << "Entity " << entity << " using spritesheet " << sprite.spriteSheet << std::endl;

		SDL_RenderCopyEx(renderer, sprite.spriteSheet, &sprite.srcRect, &sprite.destRect, sprite.angle, NULL, SDL_FLIP_NONE);
	}
}
