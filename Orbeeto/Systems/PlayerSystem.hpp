#pragma once
#include "../ECS/System.hpp"
#include "../ECS/Coordinator.hpp"


class PlayerSystem : public System {
private:
	Coordinator* coordinator;

public:
	void init(Coordinator* coord);
	Entity* checkCollision();
	void update();
};
