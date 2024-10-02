#include <vector>
#include "Vector2.hpp"


class Room {
public:
	/// <summary>
	/// Returns the room location vector
	/// </summary>
	/// <returns>The room location vector</returns>
	Vector2 getRoomLocation();
private:
	/// <summary>
	/// The room that the player is currently in on the grid of all rooms.
	/// </summary>
	Vector2 roomLocation;

	/// <summary>
	/// Can the room scroll along the x-axis?
	/// </summary>
	bool canScrollX;
	/// <summary>
	/// Can the room scroll along the x-axis?
	/// </summary>
	bool canScrollY;
};