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

	EntityID player = Game::scene.newEntity();

public:
	Room(int roomX, int roomY);

	static Camera camera;

	/// <summary>
	/// Loads all room entities.
	/// This does not include entities like enemies, bullets, or puzzle objects.
	/// </summary>
	/// <param name="x">The x-value of the room in the room grid</param>
	/// <param name="y">The y-value of the room in the room grid</param>
	void loadRoomEntities(int x, int y);
	/// <summary>
	/// Loads all entities unrelated to the room layout.
	/// Includes enemies, bullets, puzzle objects, etc.
	/// </summary>
	/// <param name="x">The x-value of the room in the room grid</param>
	/// <param name="y">The y-value of the room in the room grid</param>
	void loadOutsideEntities(int x, int y);
	void recordRoomLayout();

	void update();
};