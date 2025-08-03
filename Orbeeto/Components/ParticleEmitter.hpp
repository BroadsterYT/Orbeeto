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

	float minEmitIntensity = 3.0f;
	float maxEmitIntensity = 5.0f;


	void serialize(std::ofstream& out) override {
		uint32_t rawType = static_cast<uint32_t>(type);
		out.write(reinterpret_cast<const char*>(&rawType), sizeof(rawType));
		
		out.write(reinterpret_cast<const char*>(&buildupTime), sizeof(buildupTime));
		out.write(reinterpret_cast<const char*>(&minFreq), sizeof(minFreq));
		out.write(reinterpret_cast<const char*>(&maxFreq), sizeof(maxFreq));
		out.write(reinterpret_cast<const char*>(&nextFreq), sizeof(nextFreq));
		
		out.write(reinterpret_cast<const char*>(&minEmitIntensity), sizeof(minEmitIntensity));
		out.write(reinterpret_cast<const char*>(&maxEmitIntensity), sizeof(maxEmitIntensity));
	}

	void deserialize(std::ifstream& in) override {
		uint32_t rawType;
		in.read(reinterpret_cast<char*>(&rawType), sizeof(rawType));
		type = static_cast<PE_Type>(rawType);

		in.read(reinterpret_cast<char*>(&buildupTime), sizeof(buildupTime));
		in.read(reinterpret_cast<char*>(&minFreq), sizeof(minFreq));
		in.read(reinterpret_cast<char*>(&maxFreq), sizeof(maxFreq));
		in.read(reinterpret_cast<char*>(&nextFreq), sizeof(nextFreq));
		
		in.read(reinterpret_cast<char*>(&minEmitIntensity), sizeof(minEmitIntensity));
		in.read(reinterpret_cast<char*>(&maxEmitIntensity), sizeof(maxEmitIntensity));
	}
};