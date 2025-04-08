#pragma once


class Vector2 {
public:
	Vector2(double x = 0.0f, double y = 0.0f);
	~Vector2();

	double x, y;

	double getAngle() const;

	double getDistToPoint(const Vector2& other) const;
	/// <summary>
	/// Treating the vectors as 2D points, returns the angle between the two vectors, in degrees
	/// </summary>
	/// <param name="other">The other vector</param>
	/// <returns>The angle between the two vectors, in degrees</returns>
	double getAngleToPoint(const Vector2& other) const;
	double getAngleToPoint(const int& x, const int& y) const;
	double getMagnitude() const;

	void rotate(const double x);

	Vector2 operator+(const Vector2& other);
	Vector2 operator-(const Vector2& other);
	Vector2 operator*(const float& val);
	Vector2 operator/(const float& val);
	void operator+=(const Vector2& other);
	void operator*=(const float& val);
	bool operator==(const Vector2& other);
	bool operator!=(const Vector2& other);
};