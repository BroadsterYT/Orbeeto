#pragma once
#include <memory>
#include <string>
#include <unordered_map>
#include <vector>
#include "SDL.h"


class TextureManager {
public:
	static std::shared_ptr<SDL_Texture> loadTexture(SDL_Renderer* renderer, std::string fileName);
	static void cleanupTextures();

private:
	static std::unordered_map<std::string, std::shared_ptr<SDL_Texture>> textures;
};
