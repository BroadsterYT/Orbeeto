#pragma once
#include "SDL.h"
#include <memory>

#include "ECS/Coordinator.hpp"


class Game {
public:
	Game();
	~Game();

	void init(const char* title, int posX, int posY, int width, int height, bool fullscreen);
	
	void handleEvents();
	void update();
	void render();
	void clean();

	bool isRunning;

	SDL_Window* window;
	static SDL_Renderer* renderer;

	static Coordinator oCoordinator;
};	