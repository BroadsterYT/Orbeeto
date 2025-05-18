#pragma once
#include <string>
#include <vector>
#include <unordered_map>

#include "Vector2.hpp"
#include "Game.hpp"
#include "Camera.hpp"
#include "ECS.hpp"


class Room {
public:
	Room(int roomX, int roomY);

	static Camera camera;

	/// <summary>
	/// Retrieves the room's x-value
	/// </summary>
	/// <returns>The room's x-value</returns>
	static int getRoomX();
	/// <summary>
	/// Retrieves the room's y-value
	/// </summary>
	/// <returns>The room's y-value</returns>
	static int getRoomY();
	static int getRoomWidth();
	static int getRoomHeight();

	void loadRoom(int x, int y);
	void update();

	/// <summary>
	/// Links one portal to another. In order to create a full link, the first portal must be linked to the second, and the second linked to the first.
	/// The order of the link is important. Linking the first portal to the second means that using portal 1 will teleport you to portal 2.
	/// </summary>
	/// <param name="first">The entity ID of the first portal</param>
	/// <param name="second">The entity ID of the second portal</param>
	static void newPortalLink(Entity& first, Entity& second);
	/// <summary>
	/// Removes the link connecting one portal to another
	/// </summary>
	/// <param name="portal">The entity ID of the portal whose link should be broken</param>
	static void removePortalLink(Entity& portal);
	static Entity getPortalLink(Entity portal);
	static void clearPortalLinks();

private:
	static int roomX;
	static int roomY;
	static int roomWidth;  // Width of the room in pixels
	static int roomHeight;  // Height of the room in pixels

	bool canScrollX;
	bool canScrollY;

	int zoomOutInputCopy = 0;
	int zoomInInputCopy = 0;

	Entity player = Game::ecs.createEntity(Game::stack.peek());
	Entity leftGun = Game::ecs.createEntity(Game::stack.peek());
	Entity rightGun = Game::ecs.createEntity(Game::stack.peek());

	static std::unordered_map<Entity, Entity> portalLinks;  // Handles links between all portals

	/// <summary>
	/// Retrieves the information for each tile in a room data file
	/// </summary>
	/// <param name="roomFileName">The file path of the room data file to read from</param>
	/// <returns>The vector of room tile info</returns>
	std::vector<std::vector<uint8_t>> extractRoomTiles(const std::string roomFileName);
	/// <summary>
	/// Using tile information, constructs the tiles within the room
	/// </summary>
	/// <param name="roomTiles">A nested vector containing the room's tile IDs</param>
	void readRoomData(const std::vector<std::vector<uint8_t>> roomTiles);
	/// <summary>
	///		Creates an entity with the specified information within a tile info vector. The information in each hex value is as follows:
	///		<para>1. Tile x-axis position (in tile size, which depends on the tile set)</para>
	///		<para>2. Tile y-axis position (in tile size, which depends on the tile set)</para>
	///		<para>3. Tile width (in tile size, which depends on the tile set)</para>
	///		<para>4. Tile height (in tile size, which depends on the tile set)</para>
	///		<para>5. Tile properties</para>
	///		<para>6. Tile set</para>
	///		<para>7. Tile type</para>
	///		<para>8. Tiling style</para>
	///		<para>9. Tiles adjacent</para>
	/// </summary>
	/// <param name="tileInfo">The vector of information for the tile to be constructed with</param>
	void buildRoomEntity(const std::vector<uint8_t>& tileInfo);
};