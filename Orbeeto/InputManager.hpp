#pragma once
#include "SDL.h"

class InputManager {
public:
	InputManager();

	void init();
	void handleKeyPresses(SDL_Event event);
	void handleKeyReleases(SDL_Event event);

private:

};