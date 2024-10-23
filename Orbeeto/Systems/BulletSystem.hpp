#pragma once
#include "../ECS/System.hpp"
#include "../ECS/Coordinator.hpp"


class BulletSystem : public System {
private:
	Coordinator* coordinator;
	std::vector<Entity> kill;

public:
	void init(Coordinator* coord);
	void update();
	void killAbandoned();
};