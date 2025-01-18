#include "SpriteSystem.hpp"
#include "../Rooms/Room.hpp"
#include "../WindowManager.hpp"
#include <algorithm>


SpriteSystem::SpriteSystem(SDL_Renderer* renderer) : System() {
	SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
}

void SpriteSystem::render(SDL_Renderer* renderer) {
	SDL_SetRenderDrawColor(renderer, 0, 0, 0xFF, SDL_ALPHA_OPAQUE);
	SDL_RenderClear(renderer);

	auto entities = Game::ecs.getSystemGroup<Sprite, Transform>();
	std::vector<std::pair<int, Entity>> sortedEntities;

	for (auto& entity : entities) {
		Sprite* sprite = Game::ecs.getComponent<Sprite>(entity);
		sortedEntities.emplace_back(sprite->layer, entity);
	}

	// Custom sorting method evaluating layers
	std::sort(sortedEntities.begin(), sortedEntities.end(), 
		[](const std::pair<int, Entity>& a, const std::pair<int, Entity>& b) {
			return a.first < b.first;
		});

	for (const auto& pair : sortedEntities) {
		Entity entity = pair.second;
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

	SDL_RenderPresent(renderer);
}