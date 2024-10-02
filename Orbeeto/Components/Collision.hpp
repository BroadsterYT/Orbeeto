#pragma once
#include "../Vector2.hpp"


struct Collision {
	int hitWidth;
	int hitHeight;

	Vector2 hitPos = { 0, 0 };

	bool canMove = true;
};