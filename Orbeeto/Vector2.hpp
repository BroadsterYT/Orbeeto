#pragma once


class Vector2 {
public:
	Vector2(float x, float y);
	~Vector2();

	float x, y;

	double getAngle();

	// Treating the vectors as points, returns the angle from one to the other.
	double getAngleToPoint(const Vector2& other);
	double getAngleToPoint(const int& x, const int& y);
	double getMagnitude();

	Vector2 operator+(const Vector2& other);
	Vector2 operator-(const Vector2& other);
	Vector2 operator*(const float& val);
	void operator+=(const Vector2& other);
};