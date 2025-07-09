#include "TextRenderSystem.hpp"
#include <algorithm>
#include <fstream>
#include <iostream>
#include <stdexcept>


TextRenderSystem::TextRenderSystem() {}

void TextRenderSystem::update() {
	for (auto entity : Game::ecs.getSystemGroup<TextRender>(Game::stack.peek())) {
		TextRender* tr = Game::ecs.getComponent<TextRender>(Game::stack.peek(), entity);

		if (!tr->lineGenerated) {
			tr->lineStack = getLineFromInteraction(tr->interTag, tr->line);
			tr->lineGenerated = true;
		}

		char temp;
		if ((tr->waitTime >= tr->renderTime || tr->parsingTag) && !tr->lineStack.empty()) {
			temp = tr->lineStack.top();
			tr->lineStack.pop();

			// ----- Parsing Tags ----- //
			if (temp == '<') {
				tr->parsingTag = true;
				continue;
			}
			else if (temp == '>') {
				tr->parsingTag = false;

				// Removing tag if its opening tag is already in activeTags, otherwise adds it
				for (auto it = tr->activeTags.begin(); it != tr->activeTags.end(); ++it) {
					if ("/" + *it == tr->tagTemp) {
						tr->activeTags.erase(it);
						//std::cout << "\"" << tr->tagTemp << "\" reached and removed from activeTags" << std::endl;
						tr->tagTemp = "";
						break;
					}
				}
				if (tr->tagTemp != "") {
					tr->activeTags.push_back(tr->tagTemp);
					//std::cout << "Added tag \"" << tr->tagTemp << "\" to activeTags" << std::endl;
				}
				tr->tagTemp = "";
				continue;
			}

			if (tr->parsingTag) {
				tr->tagTemp += temp;
				continue;
			}
			// ------------------------ //

			// Creating letter entity
			Entity letter = Game::ecs.createEntity(Game::stack.peek());

			Game::ecs.assignComponent<Transform>(Game::stack.peek(), letter);
			Game::ecs.assignComponent<Sprite>(Game::stack.peek(), letter);

			Transform* ltrTrans = Game::ecs.getComponent<Transform>(Game::stack.peek(), letter);
			int w = 32;  // Width of letter sprite
			int h = 32;  // Height of letter sprite
			if (tr->letterOffset.x > tr->maxOffset.x - w / 2) {
				tr->letterOffset.x = 0;
				tr->letterOffset.y += h;
			}
			ltrTrans->pos = Vector2(400 + tr->letterOffset.x, 600 + tr->letterOffset.y);

			Sprite* ltrSprite = Game::ecs.getComponent<Sprite>(Game::stack.peek(), letter);
			*ltrSprite = Sprite(0, 0, w, h);  // Will change depending on font
			ltrSprite->spriteSheet = TextureManager::loadTexture(Game::renderer, "Assets/test_font.png");
			ltrSprite->index = (int)temp - 32;
			ltrSprite->moveWithRoom = false;
			ltrSprite->ignoreScaling = true;
			ltrSprite->layer = 1000;

			tr->letterOffset.x += w;

			// Applying movement tags
			if (hasTag(tr->activeTags, "tremble")) {
				Game::ecs.assignComponent<MovementAI>(Game::stack.peek(), letter);
				MovementAI* ai = Game::ecs.getComponent<MovementAI>(Game::stack.peek(), letter);
				ai->ai = M_AI::TEXT_TREMBLE;
				ai->vec1 = ltrTrans->pos;
				ai->mag = 5.0f;
			}

			tr->waitTime = 0.0f;
		}
		tr->waitTime += TimeManip::deltaTime;
	}
}

std::stack<char> TextRenderSystem::getLineFromInteraction(std::string interTag, int line) {
	std::ifstream file("Languages/English.txt");

	std::string temp;
	std::stack<char> output;

	bool found = false;
	while (std::getline(file, temp)) {
		if (temp == "<" + interTag + ">") {
			found = true;
			break;
		}
	}

	if (!found) {
		throw std::out_of_range("Error: Interaction tag was not found in language document.");
	}

	for (int i = 0; i <= line; i++) {
		std::getline(file, temp);
	}
	std::reverse(temp.begin(), temp.end());

	for (auto ch : temp) {
		output.push(ch);
	}

	file.close();
	return output;
}

bool TextRenderSystem::hasTag(std::vector<std::string> &tags, std::string tag) {
	int size = tags.size();
	for (int i = 0; i < size; i++) {
		if (tags[i] == tag) return true;
	}
	return false;
}