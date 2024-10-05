#pragma once
#include "../Vector2.hpp"


struct Collision {
	int hitWidth;
	int hitHeight;

	Vector2 hitPos = { 0, 0 };

	bool canMove = true;

	bool checkCollision(const Collision& check) {
		bool output = false;
		if (hitPos.x + hitWidth / 2 >= check.hitPos.x - check.hitWidth / 2
			&& hitPos.x - hitWidth / 2 <= check.hitPos.x + check.hitWidth / 2
			&& hitPos.y + hitHeight / 2 >= check.hitPos.y - check.hitHeight / 2
			&& hitPos.y - hitHeight / 2 <= check.hitPos.y + check.hitHeight / 2) {
			output = true;
		}

		return output;
	}
};