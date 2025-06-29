#define _CRTDBG_MAP_ALLOC
#include <stdlib.h>
#include <crtdbg.h>

#include <vector>
#include <algorithm>
#include <numeric>

#include "TimeManip.hpp"
#include "Game.hpp"
#include "InputManager.hpp"
#include "Room.hpp"
#include "TextureManager.hpp"
#include "WindowManager.hpp"

#include "Systems/BulletSystem.hpp"
#include "Systems/CollisionSystem.hpp"
#include "Systems/GrappleSystem.hpp"
#include "Systems/MovementAISystem.hpp"
#include "Systems/PlayerGunSystem.hpp"
#include "Systems/ParticleEmitterSystem.hpp"
#include "Systems/ParticleSystem.hpp"
#include "Systems/PlayerSystem.hpp"
#include "Systems/SpriteSystem.hpp"
#include "Systems/StatBarSystem.hpp"


Game* game = nullptr;

int main(int argc, char* argv[]) {
	int tmpFlag;

	// Get the current state of the flag
	// and store it in a temporary variable
	tmpFlag = _CrtSetDbgFlag(_CRTDBG_REPORT_FLAG);

	// Turn On (OR) - Keep freed memory blocks in the
	// heap�s linked list and mark them as freed
	tmpFlag |= _CRTDBG_LEAK_CHECK_DF;

	// Set the new state for the flag
	_CrtSetDbgFlag(tmpFlag);

	game = new Game("Orbeeto", SDL_WINDOWPOS_CENTERED, SDL_WINDOWPOS_CENTERED, Window::WIDTH, Window::HEIGHT, false);
	
	// Initializing systems
	BulletSystem bulletSystem;
	CollisionSystem collisionSystem;
	GrappleSystem grappleSystem;
	MovementAISystem movementAISystem;
	ParticleEmitterSystem PE_System;
	ParticleSystem particleSystem;
	PlayerGunSystem playerGunSystem;
	PlayerSystem playerSystem;
	SpriteSystem spriteSystem(Game::renderer);
	StatBarSystem statBarSystem;

	// Initializing room
	Room room(0, 0);

	TimeManip::previousTime = SDL_GetPerformanceCounter();

	while (game->isRunning) {
		// ---------- Handling events ---------- //
		game->handleEvents();

		// Update game components here
		spriteSystem.render(Game::renderer);
		PE_System.update();
		particleSystem.update();
		collisionSystem.update();
		playerSystem.update();
		grappleSystem.update();
		playerGunSystem.update();
		bulletSystem.update();
		movementAISystem.update();
		statBarSystem.update();

		room.update();

		Game::stack.update();
		
		TimeManip::calculateDeltaTime();
	}

	game->clean();
	_CrtDumpMemoryLeaks();
	return 0;
}