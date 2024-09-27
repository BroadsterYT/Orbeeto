#include "Game.hpp"
#include <iostream>


Game::Game() {}

Game::~Game() {}

void Game::init(const char* title, int posX, int posY, int width, int height, bool fullscreen) {
	int flags = 0;
	if (fullscreen) {
		flags = SDL_WINDOW_FULLSCREEN;
	}

	if (SDL_Init(SDL_INIT_EVERYTHING) == 0) {
		std::cout << "Subsystems initialized" << std::endl;
		window = SDL_CreateWindow("Orbeeto", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 1280, 720, flags);

		if (window) {
			std::cout << "Window created." << std::endl;
		}

		renderer = SDL_CreateRenderer(window, -1, 0);
		if (renderer) {
			SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
			std::cout << "Renderer created." << std::endl;
		}
		isRunning = true;
	}
	else {
		std::cout << "Error initializing" << std::endl;
		isRunning = false;
	}
}