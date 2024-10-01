#include "Coordinator.hpp"

#include "SpriteSystem.hpp"
#include "Sprite.hpp"


void SpriteSystem::init(Coordinator* coord) {
	coordinator = coord;
}

void SpriteSystem::render(SDL_Renderer* renderer) {
	for (const auto& entity : mEntities) {
		auto& spriteSystem = coordinator->getComponent<Sprite>(entity);

		spriteSystem.destRect.x = spriteSystem.posX;
		spriteSystem.destRect.y = spriteSystem.posY;

		SDL_RenderCopy(spriteSystem.renderer, spriteSystem.image, NULL, &spriteSystem.destRect);
	}
}