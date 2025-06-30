#include "ParticleEmitterSystem.hpp"


ParticleEmitterSystem::ParticleEmitterSystem() {}

void ParticleEmitterSystem::update() {
	for (auto entity : Game::ecs.getSystemGroup<ParticleEmitter, Transform>(Game::stack.peek())) {
		ParticleEmitter* pe = Game::ecs.getComponent<ParticleEmitter>(Game::stack.peek(), entity);
		Transform* trans = Game::ecs.getComponent<Transform>(Game::stack.peek(), entity);

		if (pe->buildupTime >= pe->nextFreq) {
			// Spawining particle
			Entity pEnt = Game::ecs.createEntity(Game::stack.peek());
			Game::ecs.assignComponent<Particle>(Game::stack.peek(), pEnt);
			Game::ecs.assignComponent<Sprite>(Game::stack.peek(), pEnt);
			Game::ecs.assignComponent<Transform>(Game::stack.peek(), pEnt);

			Particle* pcl = Game::ecs.getComponent<Particle>(Game::stack.peek(), pEnt);
			Sprite* pclSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), pEnt);
			Transform* pclTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), pEnt);

			pclSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/orbeeto.png");
			pclTrans->pos = trans->pos;

			// Random angle selection
			std::uniform_real_distribution<float> angleDist(0, 360);

			switch (pe->type) {
			case PE_Type::FULL_SCATTER:
				pclTrans->vel.x = -5;
				pclTrans->vel.rotate(angleDist(TimeManip::prng));
				break;

			default:
				break;
			}

			pe->buildupTime = 0.0f;
			std::uniform_real_distribution<float> respawnDist(pe->minFreq, pe->maxFreq);
			pe->nextFreq = respawnDist(TimeManip::prng);
		}
		pe->buildupTime += TimeManip::deltaTime;
	}
}