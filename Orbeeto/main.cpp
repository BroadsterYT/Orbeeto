#include <iostream>
#include <vector>

#include "Game.hpp"
#include "InputManager.hpp"
#include "TextureManager.hpp"

#include "ECS/Coordinator.hpp"
#include "ECS/Sprite.hpp"
#include "ECS/SpriteSystem.hpp"


SDL_Window* window;
SDL_Renderer* renderer;
bool isRunning;
bool fullscreen = false;

Coordinator oCoordinator;

Game* game = nullptr;

int main(int argc, char* argv[]) {
	const int FPS = 120;
	const int frameDelay = 1000 / FPS;

	Uint32 frameStart;
	int frameTime;

	game = new Game();
	game->init("Orbeeto", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, false);


	oCoordinator.init();
	// A vector containing all entities in the game
	std::vector<Entity> entities(MAX_ENTITIES - 1);

	// Registering components
	oCoordinator.registerComponent<Sprite>();


	// ----- Registering systems ----- //

	auto spriteSystem = oCoordinator.registerSystem<SpriteSystem>();
	{
		Signature signature;
		signature.set(oCoordinator.getComponentType<Sprite>());

		oCoordinator.setSystemSignature<SpriteSystem>(signature);
	}
	spriteSystem->init();

	// ------------------------------- //


	// Creating a test player
	const Entity& player = oCoordinator.createEntity();
	oCoordinator.addComponent<Sprite>(player, Sprite{ renderer, "assets/orbeeto.png", 64, 64, 0, 0 });


	while (isRunning) {

		frameStart = SDL_GetTicks();

		// ---------- Handling events ---------- //
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

		default:
			break;
		}

		// Update game components here

		
		// Rendering
		SDL_RenderClear(renderer);
		spriteSystem->render(renderer);

		SDL_RenderPresent(renderer);

		frameTime = SDL_GetTicks() - frameStart;  // Time in ms it takes to handle events, update, and render

		// If all updates finish sooner than the delay time, SDL will wait to render
		if (frameDelay > frameTime) {
			SDL_Delay(frameDelay - frameTime);
		}
	}

	SDL_DestroyWindow(window);
	SDL_DestroyRenderer(renderer);
	SDL_Quit();
	std::cout << "Game cleaned." << std::endl;

	return 0;
}