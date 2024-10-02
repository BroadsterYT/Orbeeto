#include <iostream>
#include <vector>

#include "Game.hpp"
#include "InputManager.hpp"
#include "TextureManager.hpp"

#include "ECS/Coordinator.hpp"
#include "Components/Sprite.hpp"
#include "Components/AccelTransform.hpp"
#include "Components/Player.hpp"
#include "Systems/AccelTransformSystem.hpp"
#include "Systems/PlayerSystem.hpp"
#include "Systems/SpriteSystem.hpp"


Game* game = nullptr;

int main(int argc, char* argv[]) {
	const int FPS = 120;
	const int frameDelay = 1000 / FPS;

	Uint32 frameStart;
	int frameTime;

	game = new Game();
	game->init("Orbeeto", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 800, 600, false);

	// Registering components
	Game::coordinator.registerComponent<Sprite>();
	Game::coordinator.registerComponent<AccelTransform>();
	Game::coordinator.registerComponent<Player>();


	// ----- Registering systems ----- //

	auto spriteSystem = Game::coordinator.registerSystem<SpriteSystem>();
	{
		Signature signature;
		signature.set(Game::coordinator.getComponentType<Sprite>());

		Game::coordinator.setSystemSignature<SpriteSystem>(signature);
	}
	spriteSystem->init(&Game::coordinator);

	auto accelTransformSystem = Game::coordinator.registerSystem<AccelTransformSystem>();
	{
		Signature signature;
		signature.set(Game::coordinator.getComponentType<AccelTransform>());

		Game::coordinator.setSystemSignature<AccelTransformSystem>(signature);
	}
	accelTransformSystem->init(&Game::coordinator);

	auto playerSystem = Game::coordinator.registerSystem<PlayerSystem>();
	{
		Signature signature;
		signature.set(Game::coordinator.getComponentType<Sprite>());
		signature.set(Game::coordinator.getComponentType<AccelTransform>());

		Game::coordinator.setSystemSignature<PlayerSystem>(signature);
	}
	playerSystem->init(&Game::coordinator);

	// ------------------------------- //


	// Creating a test player
	const Entity& player = Game::coordinator.createEntity();
	Game::coordinator.addComponent<Sprite>(player, Sprite{ Game::renderer, "assets/orbeeto.png", 64, 64, 0, 0 });
	Game::coordinator.addComponent<AccelTransform>(player, 
		AccelTransform{
			.pos = Vector2(300, 300)
		}
	);
	Game::coordinator.addComponent<Player>(player, Player{});


	while (game->isRunning) {

		frameStart = SDL_GetTicks();

		// ---------- Handling events ---------- //
		game->handleEvents();

		// Update game components here
		playerSystem->update();
		
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

	game->clean();

	return 0;
}