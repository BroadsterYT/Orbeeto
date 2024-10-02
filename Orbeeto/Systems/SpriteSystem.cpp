#include "SpriteSystem.hpp"
#include "../Components/Sprite.hpp"


void SpriteSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void SpriteSystem::render(SDL_Renderer* renderer) {
	for (const auto& entity : mEntities) {
		auto& sprite = coordinator->getComponent<Sprite>(entity);

		SDL_RenderCopy(sprite.renderer, sprite.image, NULL, &sprite.destRect);
	}
}