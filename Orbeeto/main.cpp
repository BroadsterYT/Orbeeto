#include <iostream>
#include <vector>

#include "Game.hpp"
#include "InputManager.hpp"
#include "TextureManager.hpp"

#include "ECS/Coordinator.hpp"
#include "Components/AccelTransform.hpp"
#include "Components/Collision.hpp"
#include "Components/Player.hpp"
#include "Components/Sprite.hpp"
#include "Systems/CollisionSystem.hpp"
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
	Game::coordinator.registerComponent<AccelTransform>();
	Game::coordinator.registerComponent<Collision>();
	Game::coordinator.registerComponent<Player>();
	Game::coordinator.registerComponent<Sprite>();


	// ----- Registering systems ----- //

	auto collisionSystem = Game::coordinator.registerSystem<CollisionSystem>();
	{
		Signature signature;
		signature.set(Game::coordinator.getComponentType<AccelTransform>());
		signature.set(Game::coordinator.getComponentType<Collision>());

		Game::coordinator.setSystemSignature<CollisionSystem>(signature);
	}
	collisionSystem->init(&Game::coordinator);

	auto playerSystem = Game::coordinator.registerSystem<PlayerSystem>();
	{
		Signature signature;
		signature.set(Game::coordinator.getComponentType<Sprite>());
		signature.set(Game::coordinator.getComponentType<AccelTransform>());

		Game::coordinator.setSystemSignature<PlayerSystem>(signature);
	}
	playerSystem->init(&Game::coordinator);

	auto spriteSystem = Game::coordinator.registerSystem<SpriteSystem>();
	{
		Signature signature;
		signature.set(Game::coordinator.getComponentType<Sprite>());

		Game::coordinator.setSystemSignature<SpriteSystem>(signature);
	}
	spriteSystem->init(&Game::coordinator);

	// ------------------------------- //


	// Creating a test player
	const Entity& player = Game::coordinator.createEntity();
	Game::coordinator.addComponent<Sprite>(player,
		Sprite{
			Game::renderer,
			"assets/orbeeto.png",
			64,
			64,
			0,
			0 
		}
	);
	Game::coordinator.addComponent<AccelTransform>(player, 
		AccelTransform{
			.pos = Vector2(300, 300)
		}
	);
	Game::coordinator.addComponent<Player>(player,Player{});
	Game::coordinator.addComponent<Collision>(player,
		Collision{
			64,		// hitbox width
			64,		// hitbox height
			Vector2(300, 300)	// hitbox position
		}
	);


	while (game->isRunning) {

		frameStart = SDL_GetTicks();

		// ---------- Handling events ---------- //
		game->handleEvents();

		// Update game components here
		playerSystem->update();
		collisionSystem->update();
		
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