#pragma once
#include "../ECS.hpp"
#include "../Components/Sprite.hpp"
#include "../Components/Transform.hpp"


void SpriteSystem(Scene& scene, SDL_Renderer* renderer) {
	for (EntityID entity : SceneView<Sprite, Transform>(scene)) {
		Sprite* sprite = scene.get<Sprite>(entity);
		Transform* transform = scene.get<Transform>(entity);

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