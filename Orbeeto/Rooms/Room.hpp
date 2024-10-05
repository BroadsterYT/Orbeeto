#include <vector>
#include "../Vector2.hpp"
#include "../Game.hpp"
#include "../Camera.hpp"


class Room {
private:
	int roomX;
	int roomY;

	bool canScrollX;
	bool canScrollY;

	const Entity& player = Game::coordinator.createEntity();
	const Entity& wall = Game::coordinator.createEntity();

public:
	Room(int roomX, int roomY);

	static Camera camera;

	void loadRoomLayout(int x, int y);
	void recordRoomLayout();

	void update();
};