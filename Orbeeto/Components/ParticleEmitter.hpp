#pragma once
#include "Component.hpp"


enum class PE_Type {
	FULL_SCATTER,
};


struct ParticleEmitter : Component {
	PE_Type type = PE_Type::FULL_SCATTER;
	
	float buildupTime = 0.0f;
	float minFreq = 0.1f;
	float maxFreq = 0.5f;
	float nextFreq = 1.0f;
};