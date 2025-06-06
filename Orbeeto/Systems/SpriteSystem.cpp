#include "SpriteSystem.hpp"
#include "../Room.hpp"
#include "../WindowManager.hpp"
#include <algorithm>
#include "SDL.h"
#include "../Game.hpp"


SpriteSystem::SpriteSystem(SDL_Renderer* renderer) : System() {
	SDL_SetRenderDrawBlendMode(renderer, SDL_BLENDMODE_BLEND);
	SDL_SetRenderDrawColor(renderer, 0, 0, 0xFF, SDL_ALPHA_OPAQUE);

	renderBuffer = SDL_CreateTexture(Game::renderer, SDL_PIXELFORMAT_RGBA8888, SDL_TEXTUREACCESS_TARGET, Window::WIDTH * 2, Window::HEIGHT * 2); 
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

	float scale = -(1.0 / 2560.0) * Room::camera.getWidth() + 1;

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

		// Adjusting for buffer's double size without changing sprite's location
		SDL_Rect trueDestRect = sprite->destRect;
		trueDestRect.x += Window::WIDTH / 2;
		trueDestRect.y += Window::HEIGHT / 2;

		//SDL_RenderCopyEx(renderer, sprite->spriteSheet, &sprite->srcRect, &trueDestRect, sprite->angle, NULL, SDL_FLIP_NONE);

		if (sprite->destRect.x >= spriteClip(true, true, scale) - sprite->tileWidth &&
			sprite->destRect.x <= spriteClip(true, false, scale) + sprite->tileWidth  &&
			sprite->destRect.y >= spriteClip(false, true, scale) - sprite->tileHeight &&
			sprite->destRect.y <= spriteClip(false, false, scale) + sprite->tileHeight) {
			SDL_RenderCopyEx(renderer, sprite->spriteSheet, &sprite->srcRect, &trueDestRect, sprite->angle, NULL, SDL_FLIP_NONE);
		}
	}

	SDL_SetRenderTarget(Game::renderer, NULL);
	SDL_Rect srcRect = {
		0,
		0,
		Window::WIDTH * 2,
		Window::HEIGHT * 2,
	};
	SDL_Rect destRect = {
		(Room::camera.getWidth() - Window::WIDTH) / 2,
		(Room::camera.getHeight() - Window::HEIGHT) / 2,
		Window::WIDTH + (Window::WIDTH - Room::camera.getWidth()),
		Window::HEIGHT + (Window::HEIGHT - Room::camera.getHeight())
	};
	SDL_RenderCopy(Game::renderer, renderBuffer, &srcRect, &destRect);
	SDL_RenderPresent(renderer);
}

int SpriteSystem::spriteClip(bool width, bool lower, float scale) {
	int dim = (width) ? Window::WIDTH : Window::HEIGHT;
	int mult = (lower) ? -1 : 1;
	return mult * dim / (2 * scale) + dim / 2;
}