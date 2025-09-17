#pragma once
#include <fstream>
#include <string>


class ParsingHelper {
	/// <summary>
	/// Given a tag to search for within a given file stream, returns the text within it
	/// </summary>
	/// <param name="in">The input file stream to read from</param>
	/// <param name="headerTag">The tag to search for text within</param>
	/// <returns>The text within the header tag</returns>
	static std::string getBodyData(std::ifstream& in, const std::string headerTag);
};