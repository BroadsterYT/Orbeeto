#pragma once
#include "Component.hpp"


enum class PE_Type {
	full_scatter,
};


struct ParticleEmitter : Component {
	PE_Type type = PE_Type::full_scatter;
	
	float buildupTime = 0.0f;
	float minFreq = 0.1f;
	float maxFreq = 0.5f;
	float nextFreq = 1.0f;

	float minEmitIntensity = 3.0f;
	float maxEmitIntensity = 5.0f;


	void serialize(std::ofstream& out) override {
		uint32_t rawType = static_cast<uint32_t>(type);
		SerialHelper::serialize(out, &rawType);

		SerialHelper::serialize(out, &buildupTime, &minFreq, &maxFreq, &nextFreq, &minEmitIntensity, &maxEmitIntensity);
	}

	void deserialize(std::ifstream& in) override {
		uint32_t rawType;
		SerialHelper::deserialize(in, &rawType);
		type = static_cast<PE_Type>(rawType);

		SerialHelper::deserialize(in, &buildupTime, &minFreq, &maxFreq, &nextFreq, &minEmitIntensity, &maxEmitIntensity);
	}
};