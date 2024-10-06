#pragma once
#include <cmath>
#include "Vector2.hpp"
#include <SDL_stdinc.h>


Vector2::Vector2(float x, float y) {
	this->x = x;
	this->y = y;
}

Vector2::~Vector2() {}

double Vector2::getAngle() {
	double answerRad = atan2(y, x);
	return answerRad * (180.0 / M_PI);
}

double Vector2::getDistToPoint(const Vector2& other) {
	return sqrt(pow(other.x - x, 2) + pow(other.y - y, 2));
}

double Vector2::getAngleToPoint(const Vector2& other) {
	double answerRad = atan2(x - other.x, y - other.y);
	return answerRad * (180.0 / M_PI);
}

double Vector2::getAngleToPoint(const int& x, const int& y) {
	double answerRad = atan2(this->x - x, this->y - y);
	return answerRad * (180.0 / M_PI);
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
