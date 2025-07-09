#pragma once
#include <stack>
#include "System.hpp"


class TextRenderSystem : public System {
public:
	TextRenderSystem();

	void update();

private:
	/// <summary>
	/// Finds a line from a given interaction tag and returns it in reverse inside of a stack.
	/// </summary>
	/// <param name="interTag">The interaction tag to find </param>
	/// <param name="line">The line from the interaction to read. NOTE: WIll read from different interactions if line lies beyond the desired interaction</param>
	/// <returns></returns>
	std::stack<char> getLineFromInteraction(std::string interTag, int line);
	bool hasTag(std::vector<std::string> &tags, std::string tag);
};