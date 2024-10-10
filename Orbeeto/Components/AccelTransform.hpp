#pragma once
#include "../Vector2.hpp"


struct AccelTransform {
	Vector2 pos = { 0.0f, 0.0f };
	Vector2 vel = { 0.0f, 0.0f };
	Vector2 accel = { 0.0f, 0.0f };
	float accelConst = 0.108f;
	float velConst = 10.0f;  // Velocity constant for entities moving with constant velocity

	float fric = -0.03;

	void accelMovement() {
		accel.x += vel.x * fric;
		accel.y += vel.y * fric;
		vel += accel;
		pos += vel + accel * accelConst;
	}
};