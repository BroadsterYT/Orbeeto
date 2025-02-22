#include <iostream>

#include "InputManager.hpp"


std::unordered_map<int, bool> InputManager::keysPressed{
	{SDLK_w, false},
	{SDLK_a, false},
	{SDLK_s, false},
	{SDLK_d, false},
	{SDLK_o, false},
	{SDLK_p, false},
};

std::unordered_map<int, unsigned int> InputManager::keysReleased{
	{SDLK_w, 0},
	{SDLK_a, 0},
	{SDLK_s, 0},
	{SDLK_d, 0},
	{SDLK_o, 0},
	{SDLK_p, 0},
};

std::unordered_map<int, bool> InputManager::mousePressed{
	{SDL_BUTTON_LEFT, false},
	{SDL_BUTTON_MIDDLE, false},
	{SDL_BUTTON_RIGHT, false},
};

std::unordered_map<int, unsigned int> InputManager::mouseReleased{
	{SDL_BUTTON_LEFT, 0},
	{SDL_BUTTON_MIDDLE, 0},
	{SDL_BUTTON_RIGHT, 0},
};

int InputManager::mousePosX = 0;
int InputManager::mousePosY = 0;

void InputManager::handleKeyPresses(SDL_Event event) {
	keysPressed[event.key.keysym.sym] = true;
}

void InputManager::handleKeyReleases(SDL_Event event) {
	keysPressed[event.key.keysym.sym] = false;
	keysReleased[event.key.keysym.sym]++;
}

void InputManager::handleMousePresses(SDL_Event event) {
	switch (event.button.button) {
	case SDL_BUTTON_LEFT:
		mousePressed[SDL_BUTTON_LEFT] = true;
		break;

	case SDL_BUTTON_MIDDLE:
		mousePressed[SDL_BUTTON_MIDDLE] = true;
		break;

	case SDL_BUTTON_RIGHT:
		mousePressed[SDL_BUTTON_RIGHT] = true;
		break;

	default:
		break;
	}
}

void InputManager::handleMouseReleases(SDL_Event event) {
	switch (event.button.button) {
	case SDL_BUTTON_LEFT:
		mousePressed[SDL_BUTTON_LEFT] = false;
		mouseReleased[SDL_BUTTON_LEFT]++;
		break;

	case SDL_BUTTON_MIDDLE:
		mousePressed[SDL_BUTTON_MIDDLE] = false;
		mouseReleased[SDL_BUTTON_MIDDLE]++;
		break;

	case SDL_BUTTON_RIGHT:
		mousePressed[SDL_BUTTON_RIGHT] = false;
		mouseReleased[SDL_BUTTON_RIGHT]++;
		break;

	default:
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