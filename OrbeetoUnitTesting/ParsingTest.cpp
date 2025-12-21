#include "pch.h"
#include "../../Orbeeto/Orbeeto/ParsingHelper.hpp"

#include <fstream>
#include <string>


TEST(Parsing, BodyCheck) {
	std::ifstream in("C:/Users/BroDe/source/repos/Orbeeto/OrbeetoUnitTesting/testing_files/parsing_test.txt");

	ASSERT_EQ(in.is_open(), true);
	
	std::string got = ParsingHelper::getBodyData(in, "test_header");
	std::string expected = "This line should be read.\nThis line should be read, too.\nThis line should also be included.";
	ASSERT_EQ(got, expected);

	in.close();
}