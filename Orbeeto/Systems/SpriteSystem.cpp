#include "SpriteSystem.hpp"
#include "../Components/Sprite.hpp"


void SpriteSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void SpriteSystem::render(SDL_Renderer* renderer) {
	for (const auto& entity : mEntities) {
		auto& sprite = coordinator->getComponent<Sprite>(entity);

		SDL_RenderCopyEx(sprite.renderer, sprite.image, NULL, &sprite.destRect, sprite.angle, NULL, SDL_FLIP_NONE);
	}
}