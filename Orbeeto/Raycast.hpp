#pragma once
#include <vector>
#include "Entity.hpp"
#include "Vector2.hpp"
#include "Systems/CollisionSystem.hpp"


class Raycast {
public:
	Raycast(Vector2 origin = Vector2(), int width = 16, double angle = 0.0);

	/// <summary>
	/// Collects all entities that the raycast intersects with. Vector is filled from closest to furthest from origin
	/// </summary>
	/// <param name="intersects"></param>
	void getAllIntersects();

private:
	Vector2 origin;
	Vector2 rotDir;
	double angle;  // 0 degrees is pointing north, rotation is clockwise
	int width;

	/// <summary>
	/// Returns the size difference of the collision detection's width to account for angled ray
	/// </summary>
	/// <returns></returns>
	double getWidthAdj();
};