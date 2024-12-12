#pragma once
#include "ECS.hpp"
#include "EntityGroup.hpp"
#include "SDL.h"
#include <memory>


class Game {
public:
	Game(const char* title, int posX, int posY, int width, int height, bool fullscreen);
	~Game();

	SDL_Window* window;
	static SDL_Renderer* renderer;
	static ECS ecs;

	static EntityGroup gProjectiles;
	
	void handleEvents();
	void update();
	void clean();

	bool isRunning;
};	