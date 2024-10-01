#include <iostream>
#include <vector>

#include "Game.hpp"
#include "InputManager.hpp"
#include "TextureManager.hpp"

#include "ECS/Coordinator.hpp"
#include "ECS/Sprite.hpp"
#include "ECS/SpriteSystem.hpp"


//SDL_Window* window;
//SDL_Renderer* renderer;
//bool isRunning;
//bool fullscreen = false;

Game* game = nullptr;

int main(int argc, char* argv[]) {
	const int FPS = 120;
	const int frameDelay = 1000 / FPS;

	Uint32 frameStart;
	int frameTime;

	game = new Game();
	game->init("Orbeeto", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, false);

	// A vector containing all entities in the game
	std::vector<Entity> entities(MAX_ENTITIES - 1);

	// Registering components
	Game::oCoordinator.registerComponent<Sprite>();


	// ----- Registering systems ----- //

	auto spriteSystem = Game::oCoordinator.registerSystem<SpriteSystem>();
	{
		Signature signature;
		signature.set(Game::oCoordinator.getComponentType<Sprite>());

		Game::oCoordinator.setSystemSignature<SpriteSystem>(signature);
	}
	spriteSystem->init(&Game::oCoordinator);

	// ------------------------------- //


	// Creating a test player
	const Entity& player = Game::oCoordinator.createEntity();
	Game::oCoordinator.addComponent<Sprite>(player, Sprite{ Game::renderer, "assets/orbeeto.png", 64, 64, 0, 0 });


	while (game->isRunning) {

		frameStart = SDL_GetTicks();

		// ---------- Handling events ---------- //
		game->handleEvents();

		// Update game components here

		
		// Rendering
		SDL_RenderClear(Game::renderer);
		spriteSystem->render(Game::renderer);

		SDL_RenderPresent(Game::renderer);

		frameTime = SDL_GetTicks() - frameStart;  // Time in ms it takes to handle events, update, and render

		// If all updates finish sooner than the delay time, SDL will wait to render
		if (frameDelay > frameTime) {
			SDL_Delay(frameDelay - frameTime);
		}
	}

	SDL_DestroyWindow(game->window);
	SDL_DestroyRenderer(Game::renderer);
	SDL_Quit();
	std::cout << "Game cleaned." << std::endl;

	return 0;
}