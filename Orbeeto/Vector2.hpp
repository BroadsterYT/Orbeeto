#pragma once


class Vector2 {
public:
	Vector2(float x = 0.0f, float y = 0.0f);
	~Vector2();

	float x, y;

	double getAngle();

	double getDistToPoint(const Vector2& other);
	/// <summary>
	/// Treating the vectors as 2D points, returns the angle between the two vectors, in degrees
	/// </summary>
	/// <param name="other">The other vector</param>
	/// <returns>The angle between the two vectors, in degrees</returns>
	double getAngleToPoint(const Vector2& other);
	double getAngleToPoint(const int& x, const int& y);
	double getMagnitude();

	void rotate(const double x);

	Vector2 operator+(const Vector2& other);
	Vector2 operator-(const Vector2& other);
	Vector2 operator*(const float& val);
	void operator+=(const Vector2& other);
};