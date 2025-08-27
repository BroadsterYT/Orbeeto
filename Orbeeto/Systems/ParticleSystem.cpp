#include "ParticleSystem.hpp"


ParticleSystem::ParticleSystem() {}

void ParticleSystem::update() {
	for (auto entity : Game::ecs.getSystemGroup<Particle, Sprite, Transform>(Game::stack.peek())) {
		Particle* pcl = Game::ecs.getComponent<Particle>(Game::stack.peek(), entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), entity);
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);

		if (pcl->lifetime <= pcl->maxLifetime) {
			switch (pcl->type) {
			case ParticleAI::away_from_center:
				trans->accelMovement();
				break;

			default:
				break;
			}
			pcl->lifetime += TimeManip::deltaTime;
		}
		else {
			Game::ecs.destroyEntity(Game::stack.peek(), entity);
		}
	}
}