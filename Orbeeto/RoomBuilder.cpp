#include "RoomBuilder.hpp"
#include <sstream>
#include <string>


RoomBuilder::RoomBuilder() {}

std::vector<std::vector<bool>> RoomBuilder::retrieveTileGrid(std::ifstream& in, int numRows) {
	std::string line;
	std::vector<std::vector<bool>> output;
	
	for (int i = 0; i < numRows; ++i) {
		std::getline(in, line);
		output.push_back(tokenizeTileGridRow(line));
	}

	return output;
}

std::vector<bool> RoomBuilder::tokenizeTileGridRow(std::string& instring) const {
	std::istringstream iss(instring);
	std::vector<bool> output;

	std::string token;
	while (iss >> token) {
		bool b = (token == "1");
		output.push_back(b);
	}

	return output;
}