#pragma once
#include <stack>
#include <string>
#include <vector>
#include "Component.hpp"


struct TextRender : Component {
	std::string interTag = "test";
	int line = 0;

	float renderTime = 0.05f;  // The amount of time to wait before rendering the next letter
	float waitTime = 0.0f;

	Vector2 letterOffset = Vector2(0, 0);
	Vector2 maxOffset = Vector2(1000, 256);

	std::stack<char> lineStack;
	bool lineGenerated = false;
	bool parsingTag = false;  // True if the system is currently parsing together a tag from lineStack
	std::string tagTemp = "";
	std::vector<std::string> activeTags;
};