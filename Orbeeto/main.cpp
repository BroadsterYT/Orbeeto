#include <vector>
#include <algorithm>
#include <numeric>

#include "DeltaTime.h"
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

const int FPS = 60;
const int frameDelay = 1000 / FPS;

const float TARGET_DELTA_TIME = 1.0f / 60.0f;  // 60 FPS


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

	DeltaTime::previousTime = SDL_GetPerformanceCounter();

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

		// Delta Time
		DeltaTime::currentTime = SDL_GetPerformanceCounter();
		DeltaTime::deltaTime = (DeltaTime::currentTime - DeltaTime::previousTime) / (float)SDL_GetPerformanceFrequency();
		DeltaTime::previousTime = DeltaTime::currentTime;

		// Update Buffer
		DeltaTime::deltaBuffer[DeltaTime::bufferIndex] = DeltaTime::deltaTime;
		DeltaTime::bufferIndex = (DeltaTime::bufferIndex) % DeltaTime::deltaBuffer.size();

		DeltaTime::avgDeltaTime = std::accumulate(DeltaTime::deltaBuffer.begin(), DeltaTime::deltaBuffer.end(), 0.0f) / DeltaTime::bufferSize;

		SDL_RenderClear(Game::renderer);
		spriteSystem.render(Game::renderer);
		SDL_RenderPresent(Game::renderer);

		//SDL_Delay(16);

		std::cout << DeltaTime::avgDeltaTime << std::endl;
		/*float frameTime = (SDL_GetPerformanceCounter() - DeltaTime::currentTime) / (float)SDL_GetPerformanceFrequency();
		if (frameTime < TARGET_DELTA_TIME) {
			while ((SDL_GetPerformanceCounter() - DeltaTime::currentTime) / (float)SDL_GetPerformanceFrequency() < TARGET_DELTA_TIME);
		}*/
	}

	game->clean();

	return 0;
}