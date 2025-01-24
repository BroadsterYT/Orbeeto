#include <vector>
#include <algorithm>
#include <numeric>

#include "TimeManip.hpp"
#include "Game.hpp"
#include "InputManager.hpp"
#include "Rooms/Room.hpp"
#include "TextureManager.hpp"
#include "WindowManager.hpp"

#include "Systems/BulletSystem.hpp"
#include "Systems/CollisionSystem.hpp"
#include "Systems/GrappleSystem.hpp"
#include "Systems/PlayerGunSystem.hpp"
#include "Systems/PlayerSystem.hpp"
#include "Systems/SpriteSystem.hpp"


Game* game = nullptr;

int main(int argc, char* argv[]) {
	game = new Game("Orbeeto", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, WindowManager::SCREENWIDTH, WindowManager::SCREENHEIGHT, false);

	// Initializing systems
	BulletSystem bulletSystem;
	CollisionSystem collisionSystem;
	GrappleSystem grappleSystem;
	PlayerGunSystem playerGunSystem;
	PlayerSystem playerSystem;
	SpriteSystem spriteSystem(Game::renderer);

	// Initializing room
	Room room(0, 0);

	TimeManip::previousTime = SDL_GetPerformanceCounter();

	while (game->isRunning) {
		// ---------- Handling events ---------- //
		game->handleEvents();

		// Update game components here
		spriteSystem.render(Game::renderer);
		collisionSystem.update();
		playerSystem.update();
		playerGunSystem.update();
		bulletSystem.update();
		grappleSystem.update();

		room.update();
		
		TimeManip::calculateDeltaTime();

		/*spriteSystem.render(Game::renderer);*/
		//SDL_RenderPresent(Game::renderer);
	}

	game->clean();

	return 0;
}