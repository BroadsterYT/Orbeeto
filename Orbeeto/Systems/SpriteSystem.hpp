#pragma once
#include "System.hpp"


class SpriteSystem : public System {
public:
	SpriteSystem() : System() {}

	void render(SDL_Renderer* renderer) {
		for (auto& entity : Game::ecs.getSystemGroup<Sprite, Transform>()) {
			Sprite* sprite = Game::ecs.getComponent<Sprite>(entity);
			Transform* transform = Game::ecs.getComponent<Transform>(entity);

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

	void update() {}
};