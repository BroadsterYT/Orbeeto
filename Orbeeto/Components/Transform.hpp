#pragma once
#include "Component.hpp"
#include "../Vector2.hpp"
#include "../TimeManip.hpp"


struct Transform : Component {
	Vector2 pos = { 0.0f, 0.0f };
	Vector2 vel = { 0.0f, 0.0f };
	Vector2 accel = { 0.0f, 0.0f };
	float accelConst = 0.07f;

	float fric = -0.03f;

	void accelMovement() {
		accel.x += vel.x * fric;
		accel.y += vel.y * fric;
		vel += accel * TimeManip::getDeltaAdjuster();
		pos += vel * TimeManip::getDeltaAdjuster() + accel * accelConst;

		accel = Vector2(0, 0);
	}

	void velMovement() {
		pos += vel * TimeManip::getDeltaAdjuster();
	}
};