#pragma once
#include "Entity.hpp"
#include "Game.hpp"


class RoomTile {
public:
	RoomTile(
		int posX, int posY, int width, int height,
		int tileSet, int subset, int style
	);

	/// <summary>
	/// Constructs the tile entity and returns it . NOTE: This should only be called after 
	/// all tile attributes are properly set!
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
	/// <summary>
	/// Sets whether or not the tile can have portals spawn on it
	/// </summary>
	/// <param name="canHold">True if portals can spawn on tile, false otherwise</param>
	void setCanHoldPortal(bool canHold);

private:
	int posX;
	int posY;
	int width;
	int height;

	int tileSet;
	int subset;
	int style;  // Tesselation style

	/// <summary>
	/// Performs the basic tiling scheme given a tile sheet without multiple animation frames
	/// </summary>
	/// <param name="style">The tesselation style to use</param>
	/// <param name="tileSize">The size of each individual tile in the tile sheet</param>
	/// <param name="tileSheet">The original tile sheet to use to create the final image</param>
	/// <param name="srcRect">The Rect to use as the source</param>
	/// <param name="destRect">The Rect to use as the destination</param>
	void noAnimTilingScheme1(int style, int tileSize, SDL_Texture* tileSheet, SDL_Rect& srcRect, SDL_Rect& destRect);

	// Tile properties
	bool solid = true;  // Toggles collision
	bool invisible = false;
	bool canHoldPortal = true;
};