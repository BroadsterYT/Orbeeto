#pragma once
#include "Entity.hpp"


class RoomTile {
public:
	RoomTile(
		int posX, int posY, int width, int height,
		int tileSet, int subset, int style
	);

	/// <summary>
	/// Constructs the tile entity and returns it
	/// </summary>
	/// <returns>The created tile</returns>
	Entity buildTile();

	/// <summary>
	/// Sets the tile to be solid (engage in collision) or not.
	/// </summary>
	/// <param name="isSolid">The state to set the solid property to</param>
	void setSolid(bool isSolid);
	/// <summary>
	/// Sets the state of the tile to be invisible or not.
	/// </summary>
	/// <param name="isInvis">The state to set the invisible property to</param>
	void setInvisibility(bool isInvis);

private:
	int posX;
	int posY;
	int width;
	int height;

	int tileSet;
	int subset;
	int style;  // Tiling style

	// Tile properties
	bool solid = true;  // Toggles collision
	bool invisible = false;
};