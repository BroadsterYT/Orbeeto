#pragma once
#include "TextureManager.hpp"
#include "SDL_image.h"


SDL_Texture* TextureManager::loadTexture(SDL_Renderer* renderer,  const char* fileName) {
	SDL_Surface* tempSurface = IMG_Load(fileName);
	SDL_Texture* finalTexture = SDL_CreateTextureFromSurface(renderer, tempSurface);
	SDL_FreeSurface(tempSurface);

	return finalTexture;
}
