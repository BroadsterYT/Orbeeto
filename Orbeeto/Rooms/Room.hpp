#pragma once
#include <string>
#include <vector>

#include "../Vector2.hpp"
#include "../Game.hpp"
#include "../Camera.hpp"
#include "../ECS.hpp"


class Room {
private:
	int roomX;
	int roomY;

	bool canScrollX;
	bool canScrollY;

	std::vector<Entity> currentRoomEntities;

	Entity player = Game::ecs.createEntity();
	Entity leftGun = Game::ecs.createEntity();
	Entity rightGun = Game::ecs.createEntity();

	/// <summary>
	/// Reads the values of the room details and returns them as a vector
	/// </summary>
	/// <param name="roomFilePath">The file path of the room data file to read</param>
	/// <returns>A vector of integers containing room details</returns>
	std::vector<int> vectorizeRoomDetails(const std::string roomFilePath);
	/// <summary>
	/// Pulls the tile IDs of a room's .dat file and places them into a nested vector
	/// </summary>
	/// <param name="roomFileName">The file path of the room data file to read from</param>
	/// <returns>The nested vector of room tiles</returns>
	std::vector<std::vector<int>> vectorizeRoomTiles(const std::string roomFileName);
	/// <summary>
	/// Constructs the entities within a room given vectors of the room details and tile IDs
	/// </summary>
	/// <param name="roomDetails">A vector of room details</param>
	/// <param name="roomTiles">A nested vector containing the room's tile IDs</param>
	void readRoomData(const std::vector<int> roomDetails, const std::vector<std::vector<int>> roomTiles);
	/// <summary>
	/// Creates the entities associated with a given tile ID from a room layout file
	/// </summary>
	/// <param name="tileId">The ID of the tile to construct</param>
	/// <param name="tilePosX">The x-axis position (in TILES) of where to place the tile</param>
	/// <param name="tilePosY">The y-axis position (in TILES) of where to place the tile</param>
	void buildRoomEntity(const int tileId, int tilePosX, int tilePosY);

public:
	Room(int roomX, int roomY);

	static Camera camera;

	void loadRoom(int x, int y);
	void update();
};