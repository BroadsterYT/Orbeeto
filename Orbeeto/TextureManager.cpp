#pragma once
#include "TextureManager.hpp"
#include "SDL_image.h"
#include <iostream>


std::unordered_map<std::string, std::shared_ptr<SDL_Texture>> TextureManager::textures;

std::shared_ptr<SDL_Texture> TextureManager::loadTexture(SDL_Renderer* renderer,  std::string fileName) {
	auto it = textures.find(fileName);
	if (it != textures.end()) {
		return it->second;
	}
	
	SDL_Surface* tempSurface = IMG_Load(fileName.c_str());
	SDL_Texture* rawTexture = SDL_CreateTextureFromSurface(renderer, tempSurface);
	SDL_FreeSurface(tempSurface);

	std::shared_ptr<SDL_Texture> texture(rawTexture, [](SDL_Texture* tex) {
		SDL_DestroyTexture(tex);
		});

	textures[fileName] = texture;
	return texture;
}

void TextureManager::cleanupTextures() {
	for (auto it = textures.begin(); it != textures.end(); ) {
		if (it->second.use_count() == 1) {
			it = textures.erase(it);
			std::cout << "Texture was deleted\n";
		}
		else {
			it++;
		}
	}
}
