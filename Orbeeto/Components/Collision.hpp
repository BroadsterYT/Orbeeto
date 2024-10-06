#pragma once
#include "../Vector2.hpp"
#include <iostream>
#include <SDL_stdinc.h>


struct Collision {
	int hitWidth;
	int hitHeight;

	Vector2 hitPos = { 0, 0 };

	bool canMove = true;

	/// <summary>
	/// Checks if the hitbox is colliding with another hitbox.
	/// </summary>
	/// <param name="check">The other collision component to check for a collision with</param>
	/// <returns>True if colliding, false otherwise</returns>
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

	/// <summary>
	/// Returns the side that this hitbox collided with another. NOTE: this should only be used after
	/// a collision is detected!
	/// </summary>
	/// <param name="check">The collision component to compare to</param>
	/// <returns>
	/// 0: This hitbox hit the other from the south
	/// 1: from the east
	/// 2: from the north
	/// 3: from the west</returns>
	int triangleCollide(const Collision& check) {
		// Bottom right corner of check
		Vector2 a(check.hitPos.x + check.hitWidth / 2, check.hitPos.y + check.hitHeight / 2);
		// Top right corner of check
		Vector2 b(check.hitPos.x + check.hitWidth / 2, check.hitPos.y - check.hitHeight / 2);
		// Top left corner of check
		Vector2 c(check.hitPos.x - check.hitWidth / 2, check.hitPos.y - check.hitHeight / 2);
		// Bottom left corner of check
		Vector2 d(check.hitPos.x - check.hitWidth / 2, check.hitPos.y + check.hitHeight / 2);

		double angleA = (M_PI / 180.0) * hitPos.getAngleToPoint(a);
		double angleB = (M_PI / 180.0) * hitPos.getAngleToPoint(b);
		double angleC = (M_PI / 180.0) * hitPos.getAngleToPoint(c);
		double angleD = (M_PI / 180.0) * hitPos.getAngleToPoint(d);

		double heightA = abs(hitPos.getDistToPoint(a) * sin(angleA));
		double heightB = abs(hitPos.getDistToPoint(b) * cos(angleB));
		double heightC = abs(hitPos.getDistToPoint(c) * sin(angleC));
		double heightD = abs(hitPos.getDistToPoint(d) * cos(angleD));

		double heights[4] = { heightA, heightB, heightC, heightD };
		int smallest = 0;
		for (int i = 0; i < 4; i++) {
			if (heights[i] < heights[smallest]) {
				smallest = i;
			}
		}

		return smallest; // Placeholder
	}
};