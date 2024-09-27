#pragma once

#include "Coordinator.hpp"

#include "SpriteSystem.hpp"
#include "Sprite.hpp"


extern Coordinator oCoordinator;


void SpriteSystem::init() {}

void SpriteSystem::render(SDL_Renderer* renderer) {
	for (const auto& entity : mEntities) {
		auto& spriteSystem = oCoordinator.getComponent<Sprite>(entity);

		spriteSystem.destRect.x = spriteSystem.posX;
		spriteSystem.destRect.y = spriteSystem.posY;

		SDL_RenderCopy(spriteSystem.renderer, spriteSystem.image, NULL, &spriteSystem.destRect);
	}
}