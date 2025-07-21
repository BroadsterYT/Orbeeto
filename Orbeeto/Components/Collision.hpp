#pragma once
#include "Component.hpp"
#include "../Vector2.hpp"
#include <cmath>
#include <iostream>
#include <SDL_stdinc.h>

enum class PTags {  // Physics tags
	CAN_PUSH,
	PUSHABLE,

	WALL,
	PLAYER,
	GRAPPLE,
	PORTAL,
	PORTAL_BULLET,

	BUTTON_TRINKET,

	CAN_HOLD_PORTAL,
	CAN_TELEPORT,
	
	PROJECTILE,
	P_PROJECTILE,  // Player projectile
	E_PROJECTILE,  // Enemy projectile

	HURTABLE,  // The entity can take damage
	ENEMY
};

struct Collision : Component {
	int hitWidth = 64;
	int hitHeight = 64;
	Vector2 hitPos = { 0, 0 };

	bool tpFlag = false;  // Lets other objects detect entity teleportation

	std::bitset<32> physicsTags = std::bitset<32>().reset();
};