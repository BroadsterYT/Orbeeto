#pragma once
#include <cmath>
#include "Vector2.hpp"


Vector2::Vector2(float x, float y) {
	this->x = x;
	this->y = y;
}

Vector2::~Vector2() {}

float Vector2::getX() {
	return x;
}

float Vector2::getY() {
	return y;
}

double Vector2::getAngle() {
	return atan2(y, x);
}

double Vector2::getMagnitude() {
	return sqrt(pow(x, 2) + pow(y, 2));
}
