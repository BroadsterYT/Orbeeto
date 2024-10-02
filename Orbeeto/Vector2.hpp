#pragma once


class Vector2 {
public:
	Vector2(float x, float y);
	~Vector2();

	float x, y;

	double getAngle();
	double getMagnitude();

	Vector2 operator+(const Vector2& other);
	Vector2 operator-(const Vector2& other);
	Vector2 operator*(const float& val);
	void operator+=(const Vector2& other);
};