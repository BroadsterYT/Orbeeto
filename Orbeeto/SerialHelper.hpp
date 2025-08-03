#pragma once
#include <fstream>
#include <type_traits>


class SerialHelper {
public:
	template<typename... Args>
	static void serialize(std::ofstream& out, Args*... args) {
		(static_cast<void>(serializeOne(out, args)), ...);
	}

	template<typename T>
	static void serializeOne(std::ofstream& out, T* val) {
		static_assert(std::is_trivially_copyable<T>::value, "Type is not trivially copyable");
		if (val) {
			out.write(reinterpret_cast<const char*>(val), sizeof(*val));
		}
	}

	template<typename... Args>
	static void deserialize(std::ifstream& in, Args*... args) {
		(static_cast<void>(deserializeOne(in, args)), ...);
	}

	template<typename T>
	static void deserializeOne(std::ifstream& in, T* val) {
		if (val) {
			in.read(reinterpret_cast<char*>(val), sizeof(*val));
		}
	}
};