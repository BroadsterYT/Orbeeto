#pragma once

#include "../Vector2.hpp"

struct AccelTransform {
	Vector2 pos;
	Vector2 vel;
	Vector2 accel;
	double accelConst = 0.58;
};