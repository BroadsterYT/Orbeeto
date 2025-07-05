#include "TextParser.hpp"


std::vector<std::string> TextParser::getInteraction(std::string id) {
    std::ifstream file("English.txt");

    std::string temp;
    std::vector<std::string> output;

    bool include = false;
    while (std::getline(file, temp)) {
        if (temp == "<" + id + ">") {
            include = true;
            continue;
        }
        if (temp == "</" + id + ">") {
            break;
        }
        if (include) {
            output.push_back(temp);
        }
    }

    file.close();
    return output;
}