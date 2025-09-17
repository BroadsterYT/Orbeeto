#pragma once
#include <vector>
#include <fstream>


class RoomBuilder {
public:
	RoomBuilder();

	/// <summary>
	/// Given a grid of boolean values, converts them into a 2d grid of values and returns the result
	/// </summary>
	/// <param name="in">The input file stream to read from</param>
	/// <param name="numRows">The number of rows the output grid will have</param>
	/// <returns>A vector containing the values arranged in rows and columns</returns>
	std::vector<std::vector<bool>> retrieveTileGrid(std::ifstream& in, int numRows);

private:
	/// <summary>
	/// Given a string of 1s and 0s separated by spaces, returns a vector containing the boolean representations of the values in order
	/// </summary>
	/// <param name="instring">The input string to tokenize from</param>
	/// <returns>A vector of booleans representing the string values</returns>
	std::vector<bool> tokenizeTileGridRow(std::string& instring) const;
};