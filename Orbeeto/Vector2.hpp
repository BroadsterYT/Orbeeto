#pragma once


class Vector2 {
private:
	float x, y;

public:
	Vector2(float x, float y);
	~Vector2();

	float getX();
	float getY();

	double getAngle();
	double getMagnitude();
};