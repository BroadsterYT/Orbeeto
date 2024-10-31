#include <iostream>
#include <vector>

#include "Game.hpp"
#include "InputManager.hpp"
#include "Rooms/Room.hpp"
#include "TextureManager.hpp"

#include "Components/Bullet.hpp"
#include "Components/Collision.hpp"
#include "Components/Defense.hpp"
#include "Components/Hp.hpp"
#include "Components/Player.hpp"
#include "Components/PlayerGun.hpp"
#include "Components/Sprite.hpp"
#include "Components/Transform.hpp"

#include "Systems/CollisionSystem.hpp"
#include "Systems/PlayerSystem.hpp"
#include "Systems/SpriteSystem.hpp"


Game* game = nullptr;
int s_componentCounter = 0;

const int FPS = 240;
const int frameDelay = 1000 / FPS;

int main(int argc, char* argv[]) {
	Uint32 frameStart;
	int frameTime;

	game = new Game("Orbeeto", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 1280, 720, false);


	// Initializing room
	Room room(0, 0);


	while (game->isRunning) {

		frameStart = SDL_GetTicks();

		// ---------- Handling events ---------- //
		game->handleEvents();

		// Update game components here
		room.update();
		CollisionSystem(Game::ecs);
		PlayerSystem(Game::ecs);

		SDL_RenderClear(Game::renderer);
		SpriteSystem(Game::renderer, Game::ecs);
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