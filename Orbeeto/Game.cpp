#include "Game.hpp"
#include "InputManager.hpp"
#include "WindowManager.hpp"
#include <iostream>


SDL_Renderer* Game::renderer = nullptr;

ECS Game::ecs = ECS();
GameStack Game::stack = GameStack();

Game::Game(const char* title, int posX, int posY, int width, int height, bool fullscreen) {
	int flags = 0;
	if (fullscreen) {
		flags = SDL_WINDOW_FULLSCREEN;
	}

	if (SDL_Init(SDL_INIT_EVERYTHING) == 0) {
		std::cout << "Subsystems initialized" << std::endl;
		window = SDL_CreateWindow(
			"Orbeeto",
			SDL_WINDOWPOS_CENTERED, 
			SDL_WINDOWPOS_CENTERED, 
			Window::WIDTH, 
			Window::HEIGHT, 
			flags
		);

		if (window) {
			std::cout << "Window created." << std::endl;
		}

		renderer = SDL_CreateRenderer(window, -1, SDL_RENDERER_TARGETTEXTURE);
		if (renderer) {
			SDL_SetRenderDrawColor(renderer, 255, 255, 255, 255);
			std::cout << "Renderer created." << std::endl;
		}
		isRunning = true;
	}
	else {
		std::cout << "Error initializing SDL2" << std::endl;
		isRunning = false;
	}
}

Game::~Game() {}

void Game::handleEvents() {
	SDL_Event event;
	SDL_PollEvent(&event);
	switch (event.type) {
	case SDL_QUIT:
		isRunning = false;
		break;

	case SDL_KEYDOWN:
		InputManager::handleKeyPresses(event);
		break;

	case SDL_KEYUP:
		InputManager::handleKeyReleases(event);
		break;

	case SDL_MOUSEMOTION:
		SDL_GetMouseState(&InputManager::mousePosX, &InputManager::mousePosY);
		break;

	case SDL_MOUSEBUTTONDOWN:
		InputManager::handleMousePresses(event);
		break;

	case SDL_MOUSEBUTTONUP:
		InputManager::handleMouseReleases(event);
		break;

	default:
		break;
	}
}

void Game::update() {
	// Rendering
}

void Game::clean() {
	SDL_DestroyWindow(window);
	SDL_DestroyRenderer(renderer);
	SDL_Quit();
	std::cout << "Game cleaned." << std::endl;
}