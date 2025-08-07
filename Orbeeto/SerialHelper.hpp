#pragma once
#include <fstream>
#include <type_traits>


class SerialHelper {
public:
	/// <summary>
	/// Serializes one or more trivially copyable values
	/// </summary>
	/// <typeparam name="...Args"></typeparam>
	/// <param name="out">The output file stream object to write to</param>
	/// <param name="...args">The (trivially copyable) values to serialize</param>
	template<typename... Args>
	static void serialize(std::ofstream& out, Args*... args) {
		(static_cast<void>(serializeOne(out, args)), ...);
	}

	/// <summary>
	/// Deserializes one or more trivially copyable values
	/// </summary>
	/// <typeparam name="...Args"></typeparam>
	/// <param name="in">The input file stream to read from</param>
	/// <param name="...args">The (trivially copyable) values to deserialize. NOTE:	Be sure to deserialize values in the same order as they were serialized</param>
	template<typename... Args>
	static void deserialize(std::ifstream& in, Args*... args) {
		(static_cast<void>(deserializeOne(in, args)), ...);
	}

	template<typename T>
	static void serializeVector(std::ofstream& out, std::vector<T>* vec) {
		static_assert(std::is_trivially_copyable<T>::value, "Vector of given type is not trivially copyable");
		if (!vec) return;
		uint32_t vecLen = vec->size();
		out.write(reinterpret_cast<const char*>(&vecLen), sizeof(vecLen));
		out.write(reinterpret_cast<const char*>(vec->data()), sizeof(T) * vecLen);
	}

	template<typename T>
	static void deserializeVector(std::ifstream& in, std::vector<T>* vec) {
		uint32_t vecLen;
		in.read(reinterpret_cast<char*>(&vecLen), sizeof(vecLen));
		vec->resize(vecLen);
		in.read(reinterpret_cast<char*>(vec->data()), sizeof(T) * vecLen);
	}

private:
	template<typename T>
	static void serializeOne(std::ofstream& out, T* val) {
		if (!val) return;

		if constexpr (std::is_same_v<T, std::string>) {
			serializeString(out, val);
		}
		else {
			static_assert(std::is_trivially_copyable<T>::value, "Type is not trivially copyable");
			out.write(reinterpret_cast<const char*>(val), sizeof(*val));
		}
	}

	template<typename T>
	static void deserializeOne(std::ifstream& in, T* val) {
		if (!val) return;

		if constexpr (std::is_same_v<T, std::string>) {
			deserializeString(in, val);
		}
		else {
			in.read(reinterpret_cast<char*>(val), sizeof(*val));
		}
	}

	static void serializeString(std::ostream& out, const std::string* str) {
		uint32_t len = static_cast<uint32_t>(str->size());
		out.write(reinterpret_cast<const char*>(&len), sizeof(len));
		out.write(str->data(), len);
	}

	static void deserializeString(std::ifstream& in, std::string* str) {
		uint32_t len;
		in.read(reinterpret_cast<char*>(&len), sizeof(len));

		str->resize(len);
		in.read(&(*str)[0], len);
	}
};