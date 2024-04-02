class LZWCompressor:
    def __init__(self):
        self.dictionary_size = 256
        self.dictionary = {chr(i): i for i in range(self.dictionary_size)}

    def compress(self, data):
        compressed_data = []
        word = ""
        for char in data:
            new_word = word + char
            if new_word in self.dictionary:
                word = new_word
            else:
                compressed_data.append(self.dictionary[word])
                self.dictionary[new_word] = self.dictionary_size
                self.dictionary_size += 1
                word = char
        if word:
            compressed_data.append(self.dictionary[word])
        return compressed_data

    def decompress(self, compressed_data):
        decompressed_data = ""
        reverse_dictionary = {v: k for k, v in self.dictionary.items()}
        prev = chr(compressed_data.pop(0))
        decompressed_data += prev
        for code in compressed_data:
            if code in reverse_dictionary:
                current = reverse_dictionary[code]
                decompressed_data += current
                self.dictionary[prev + current[0]] = self.dictionary_size
                self.dictionary_size += 1
                prev = current
            else:
                current = prev + prev[0]
                decompressed_data += current
                self.dictionary[code] = self.dictionary_size
                self.dictionary_size += 1
                prev = current
        return decompressed_data


# Приклад використання:
compressor = LZWCompressor()
data = "TEXT SAMPLE."
compressed_data = compressor.compress(data)
print("ущільнені дані:", compressed_data)

decompressed_data = compressor.decompress(compressed_data)
print("розшифровані дані:", decompressed_data)
