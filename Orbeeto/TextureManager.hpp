#pragma once
#include "SDL.h"


class TextureManager {
public:
	static SDL_Texture* loadTexture(SDL_Renderer* renderer, const char* fileName);
};
