#include <vector>
#include "../Vector2.hpp"
#include "../Game.hpp"


class Room {
private:
	int roomX;
	int roomY;

	bool canScrollX;
	bool canScrollY;

	const Entity& player = Game::coordinator.createEntity();

public:
	Room(int roomX, int roomY);

	void loadRoomLayout(int x, int y);
	void recordRoomLayout();
};