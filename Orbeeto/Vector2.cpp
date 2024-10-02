#pragma once
#include <cmath>
#include "Vector2.hpp"


Vector2::Vector2(float x = 0.0f, float y = 0.0f) {
	this->x = x;
	this->y = y;
}

Vector2::~Vector2() {}

double Vector2::getAngle() {
	return atan2(y, x);
}

double Vector2::getMagnitude() {
	return sqrt(pow(x, 2) + pow(y, 2));
}

Vector2 Vector2::operator+(const Vector2& other) {
	return Vector2(x + other.x, y + other.y);
}

Vector2 Vector2::operator-(const Vector2& other) {
	return Vector2(x - other.x, y - other.y);
}

Vector2 Vector2::operator*(const float& val) {
	return Vector2(x * val, y * val);
}

void Vector2::operator+=(const Vector2& other) {
	x += other.x;
	y += other.y;
}
