#pragma once
#include "../ECS.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Transform.hpp"
#include "../Rooms/Room.hpp"


void SpriteSystem(SDL_Renderer* renderer, ECS& ecs) {
	for (auto& entity : ecs.getSystemGroup<Sprite, Transform>()) {
		Sprite* sprite = ecs.getComponent<Sprite>(entity);
		Transform* transform = ecs.getComponent<Transform>(entity);

		if (sprite->moveWithRoom) {
			sprite->destRect.x = transform->pos.x - sprite->tileWidth / 2 - Room::camera.getX();
			sprite->destRect.y = transform->pos.y - sprite->tileHeight / 2 - Room::camera.getY();
		}
		else {
			sprite->destRect.x = transform->pos.x - sprite->tileWidth / 2;
			sprite->destRect.y = transform->pos.y - sprite->tileHeight / 2;
		}

		
		SDL_RenderCopyEx(renderer, sprite->spriteSheet, &sprite->srcRect, &sprite->destRect, sprite->angle, NULL, SDL_FLIP_NONE);
	}
}