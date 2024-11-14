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

#include "Systems/BulletSystem.hpp"
#include "Systems/CollisionSystem.hpp"
#include "Systems/PlayerGunSystem.hpp"
#include "Systems/PlayerSystem.hpp"
#include "Systems/SpriteSystem.hpp"


Game* game = nullptr;

const int FPS = 240;
const int frameDelay = 1000 / FPS;

int main(int argc, char* argv[]) {
	uint32_t frameStart;
	int frameTime;

	game = new Game("Orbeeto", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, 1280, 720, false);

	// Initializing room
	Room room(0, 0);

	// Initializing systems
	BulletSystem bulletSystem;
	CollisionSystem collisionSystem;
	PlayerGunSystem playerGunSystem;
	PlayerSystem playerSystem;
	SpriteSystem spriteSystem;


	while (game->isRunning) {
		frameStart = SDL_GetTicks();

		// ---------- Handling events ---------- //
		game->handleEvents();

		// Update game components here
		collisionSystem.update();
		playerSystem.update();
		playerGunSystem.update();

		bulletSystem.update();

		room.update();

		SDL_RenderClear(Game::renderer);
		spriteSystem.render(Game::renderer);
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