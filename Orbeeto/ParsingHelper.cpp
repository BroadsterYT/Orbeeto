#include "ParsingHelper.hpp"


std::string ParsingHelper::getBodyData(std::ifstream& in, const std::string headerTag) {
	std::string bodyText;
	
	bool read = false;
	std::string tempLine;
	while (std::getline(in, tempLine)) {
		if (tempLine == "<" + headerTag + ">") {
			read = true;
			continue;
		}
		else if (tempLine == "</" + headerTag + ">") {
			break;
		}

		if (read) {
			bodyText += tempLine + "\n";
		}
	}

	return bodyText;
}