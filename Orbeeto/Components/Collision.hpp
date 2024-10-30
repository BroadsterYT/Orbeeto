#pragma once
#include "Component.hpp"
#include "../Vector2.hpp"
#include <cmath>
#include <iostream>
#include <SDL_stdinc.h>

/// <summary>
/// A compent for detecting collisions between entities
/// </summary>
/// <param name="hitWidth">The width of the hitbox</param>
/// <param name="hitHeight">The height of the hitbox</param>
/// <param name="hitPos">The position of the center of the hitbox. Defaults to (0, 0)</param>
/// <param name="canBePushed">Can the entity be pushed by others? Defaults to true</param>
/// <param name="canPush">Can the entity push others? Defaults to true</param>
/// <param name="isProj">Should the entity be treated as a projectile? Defaults to false</param>
/// <param name="canHurt">Can the entity be hurt? Defaults to false</param>
struct Collision : Component {
	int hitWidth;
	int hitHeight;

	Vector2 hitPos = { 0, 0 };

	bool canBePushed = true;
	bool canPush = true;
	
	bool isProj = false;
	bool canHurt = false;

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
	/// Returns the side that this entity is colliding with the other. NOTE: This should
	/// only be called after a collision has been detected!
	/// </summary>
	/// <param name="other">The collision component of the entity that this one is colliding with</param>
	/// <returns>The side of the other entity that this entity hit</returns>
	int intersection(const Collision& other) {
		Vector2 dist(hitPos.x - other.hitPos.x, hitPos.y - other.hitPos.y);
		Vector2 minDist((hitWidth + other.hitWidth) / 2, (hitHeight + other.hitHeight) / 2);

		Vector2 depth;
		depth.x = dist.x > 0 ? minDist.x - dist.x : -minDist.x - dist.x;
		depth.y = dist.y > 0 ? minDist.y - dist.y : -minDist.y - dist.y;

		if (depth.x != 0 && depth.y != 0) {
			if (abs(depth.x) < abs(depth.y)) {  // Collision along x-axis
				if (depth.x > 0) return 1;
				else return 3;
			}
			else {  // Collision along y-axis
				if (depth.y > 0) return 0;
				else return 2;
			}
		}

		return -1;
	}
};