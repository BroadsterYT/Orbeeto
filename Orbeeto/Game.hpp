#pragma once
#include <memory>
#include "ECS/SpriteSystem.hpp"


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
	SDL_Renderer* renderer;

	std::shared_ptr<SpriteSystem> spriteSystem;

private:
};