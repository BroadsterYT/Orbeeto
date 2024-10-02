#include <iostream>

#include "InputManager.hpp"


std::unordered_map<int, bool> InputManager::keysPressed{
	{SDLK_w, false},
	{SDLK_a, false},
	{SDLK_s, false},
	{SDLK_d, false},
};

std::unordered_map<int, unsigned int> InputManager::keysReleased{
	{SDLK_w, 0},
	{SDLK_a, 0},
	{SDLK_s, 0},
	{SDLK_d, 0},
};

int InputManager::mousePosX = 0;
int InputManager::mousePosY = 0;

void InputManager::handleKeyPresses(SDL_Event event) {
	switch (event.key.keysym.sym) {
	case SDLK_w:
		keysPressed[SDLK_w] = true;
		break;

	case SDLK_a:
		keysPressed[SDLK_a] = true;
		break;

	case SDLK_s:
		keysPressed[SDLK_s] = true;
		break;

	case SDLK_d:
		keysPressed[SDLK_d] = true;
		break;
	}
}

void InputManager::handleKeyReleases(SDL_Event event) {
	switch (event.key.keysym.sym) {
	case SDLK_w:
		keysPressed[SDLK_w] = false;
		keysReleased[SDLK_w]++;
		break;

	case SDLK_a:
		keysPressed[SDLK_a] = false;
		keysReleased[SDLK_a]++;
		break;

	case SDLK_s:
		keysPressed[SDLK_s] = false;
		keysReleased[SDLK_s]++;
		break;

	case SDLK_d:
		keysPressed[SDLK_d] = false;
		keysReleased[SDLK_d]++;
		break;
	}
}

void InputManager::printKeysPressed() {
	for (auto& key : keysPressed) {
		std::cout << "Key: [" << key.first << "] isPressed: [" << key.second << "]" << std::endl;
	}
	std::cout << std::endl;
}

void InputManager::printKeysReleased() {
	for (auto& key : keysReleased) {
		std::cout << "Key: [" << key.first << "] Releases: [" << key.second << "]" << std::endl;
	}
	std::cout << std::endl;
}