#pragma once
#include "SDL.h"
#include "ECS.hpp"
#include <memory>


class Game {
public:
	Game(const char* title, int posX, int posY, int width, int height, bool fullscreen);
	~Game();

	SDL_Window* window;
	static SDL_Renderer* renderer;
	static ECS ecs;
	
	void handleEvents();
	void update();
	void clean();

	bool isRunning;
};	