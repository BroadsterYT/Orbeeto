#pragma once
#include "Component.hpp"


struct StatBar : public Component {
	int minVal = 0;
	int* maxVal = nullptr;
	int* val = nullptr;

	bool deleteAtZero = true;  // Should the entity with this component be destroyed when val reaches 0?

	
	// StatBars will be destroyed and recreated manually upon deserialization
};