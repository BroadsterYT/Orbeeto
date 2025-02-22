#pragma once
#include <cmath>
#include "Vector2.hpp"
#include <SDL_stdinc.h>


Vector2::Vector2(double x, double y) {
	this->x = x;
	this->y = y;
}

Vector2::~Vector2() {}

double Vector2::getAngle() const {
	double answerRad = atan2(x, y);
	return answerRad * (180.0 / M_PI);
}

double Vector2::getDistToPoint(const Vector2& other) const {
	return sqrt(pow(other.x - x, 2) + pow(other.y - y, 2));
}

double Vector2::getAngleToPoint(const Vector2& other) const {
	double answerRad = atan2(x - other.x, y - other.y);
	return answerRad * (180.0 / M_PI);
}

double Vector2::getAngleToPoint(const int& x, const int& y) const {
	double answerRad = atan2(this->x - x, this->y - y);
	return answerRad * (180.0 / M_PI);
}

double Vector2::getMagnitude() const {
	return sqrt(pow(x, 2) + pow(y, 2));
}

void Vector2::rotate(const double x) {
	const double angleRad = x * (M_PI / 180.0);
	double tempX = this->x;
	this->x = cos(angleRad) * tempX - sin(angleRad) * y;
	y = sin(angleRad) * tempX + cos(angleRad) * y;
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
