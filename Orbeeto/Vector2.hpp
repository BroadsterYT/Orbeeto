#pragma once


class Vector2 {
public:
	Vector2(float x = 0.0f, float y = 0.0f);
	~Vector2();

	float x, y;

	double getAngle();

	double getDistToPoint(const Vector2& other);
	double getAngleToPoint(const Vector2& other); // Treating the vectors as points, returns the angle from one to the other.
	double getAngleToPoint(const int& x, const int& y);
	double getMagnitude();

	void rotate(const double x);

	Vector2 operator+(const Vector2& other);
	Vector2 operator-(const Vector2& other);
	Vector2 operator*(const float& val);
	void operator+=(const Vector2& other);
};