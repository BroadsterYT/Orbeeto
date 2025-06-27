#include "ParticleSystem.hpp"


ParticleSystem::ParticleSystem() {}

void ParticleSystem::update() {
	for (auto entity : Game::ecs.getSystemGroup<Particle, Sprite, Transform>(Game::stack.peek())) {
		Particle* pcl = Game::ecs.getComponent<Particle>(Game::stack.peek(), entity);
		Sprite* sprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), entity);
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);

		if (pcl->lifetime <= pcl->maxLifetime) {
			switch (pcl->type) {
			case ParticleAI::AWAY_FROM_CENTER:
				// TODO: Correct acceleration and velocity for direction permissions (issue for ParticleEmitterSystem)

				trans->accelMovement();
				break;
			}
		}
		else {
			Game::ecs.destroyEntity(Game::stack.peek(), entity);
		}
	}
}