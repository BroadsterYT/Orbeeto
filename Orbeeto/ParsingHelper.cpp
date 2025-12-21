#include "ParsingHelper.hpp"
#include <iostream>


std::string ParsingHelper::getBodyData(std::ifstream& in, const std::string headerTag) {
	std::string bodyText;
	
	bool read = false;
	std::string tempLine;
	while (std::getline(in, tempLine)) {
		if (read) {
			bodyText += tempLine + "\n";
		}

		if (tempLine == "<" + headerTag + ">") {
			read = true;
			continue;
		}
		else if (tempLine == "</" + headerTag + ">") {
			bodyText.pop_back();  // Removing last newline character in output
			break;
		}
	}

	return bodyText;
}