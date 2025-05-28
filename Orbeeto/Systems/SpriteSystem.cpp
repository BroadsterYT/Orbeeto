#include "SpriteSystem.hpp"
#include "../Room.hpp"
#include "../WindowManager.hpp"
#include <algorithm>
#include "SDL.h"
#include "../Game.hpp"


SpriteSystem::SpriteSystem(SDL_Renderer* renderer) : System() {
	SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
	SDL_SetRenderDrawColor(renderer, 0, 0, 0xFF, SDL_ALPHA_OPAQUE);

	renderBuffer = SDL_CreateTexture(Game::renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, WindowManager::SCREENWIDTH * 2, WindowManager::SCREENHEIGHT * 2); 
	SDL_SetTextureBlendMode(renderBuffer, SDL_BLENDMODE_BLEND);
}

void SpriteSystem::render(SDL_Renderer* renderer) {
	SDL_SetRenderTarget(Game::renderer, renderBuffer);
	SDL_RenderClear(renderer);  // Clears buffer

	auto entities = Game::ecs.getSystemGroup<Sprite, Transform>(Game::stack.peek());
	std::vector<std::pair<int, Entity>> sortedEntities;

	for (auto& entity : entities) {
		Sprite* sprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), entity);
		sortedEntities.emplace_back(sprite->layer, entity);
	}

	// Custom sorting method evaluating layers
	std::sort(sortedEntities.begin(), sortedEntities.end(), 
		[](const std::pair<int, Entity>& a, const std::pair<int, Entity>& b) {
			return a.first < b.first;
		});

	for (const auto& pair : sortedEntities) {
		Entity entity = pair.second;
		Sprite* sprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), entity);
		Transform* transform = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);

		// Showing correct sprite given sprite index
		int width, height;
		SDL_QueryTexture(sprite->spriteSheet, NULL, NULL, &width, &height);
		int spritesPerRow = width / sprite->tileWidth;

		sprite->srcRect.x = sprite->index % spritesPerRow * sprite->tileWidth;
		sprite->srcRect.y = sprite->index / spritesPerRow * sprite->tileHeight;

		// TODO: Implement no-scaling functionaliity
		if (sprite->moveWithRoom) {
			sprite->destRect.x = (transform->pos.x - sprite->tileWidth / 2 - Room::camera.getX());
			sprite->destRect.y = (transform->pos.y - sprite->tileHeight / 2 - Room::camera.getY());
			sprite->destRect.w = sprite->tileWidth;
			sprite->destRect.h = sprite->tileHeight;
		}
		else {
			sprite->destRect.x = transform->pos.x - sprite->tileWidth / 2;
			sprite->destRect.y = transform->pos.y - sprite->tileHeight / 2;
		}
		SDL_RenderCopyEx(renderer, sprite->spriteSheet, &sprite->srcRect, &sprite->destRect, sprite->angle, NULL, SDL_FLIP_NONE);
	}

	//std::cout << "Room w: " << Room::camera.getWidth() << " h: " << Room::camera.getHeight() << std::endl;

	SDL_SetRenderTarget(Game::renderer, NULL);
	SDL_Rect srcRect = {
		0,
		0,
		WindowManager::SCREENWIDTH,
		WindowManager::SCREENHEIGHT,
	};
	SDL_Rect destRect = {
		(Room::camera.getWidth() - WindowManager::SCREENWIDTH) / 2,
		(Room::camera.getHeight() - WindowManager::SCREENHEIGHT) / 2,
		WindowManager::SCREENWIDTH + (WindowManager::SCREENWIDTH - Room::camera.getWidth()),
		WindowManager::SCREENHEIGHT + (WindowManager::SCREENHEIGHT - Room::camera.getHeight())
	};
	SDL_RenderCopy(Game::renderer, renderBuffer, &srcRect, &destRect);
	SDL_RenderPresent(renderer);
}