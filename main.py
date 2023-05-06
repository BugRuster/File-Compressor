import tkinter as tk
from tkinter import filedialog
import heapq
import os

class HuffmanNode:
    def __init__(self, freq, char=None):
        self.freq = freq
        self.char = char
        self.left = None
        self.right = None

    def __lt__(self, other):
        return self.freq < other.freq

    def __eq__(self, other):
        return self.freq == other.freq

class HuffmanCoding:
    def __init__(self):
        self.codes = {}
        self.reverse_mapping = {}

    def make_frequency_dict(self, text):
        freq_dict = {}
        for char in text:
            if char not in freq_dict:
                freq_dict[char] = 0
            freq_dict[char] += 1
        return freq_dict

    def make_heap(self, freq_dict):
        heap = []
        for char, freq in freq_dict.items():
            node = HuffmanNode(freq, char)
            heapq.heappush(heap, node)
        return heap

    def merge_nodes(self, heap):
        while len(heap) > 1:
            node1 = heapq.heappop(heap)
            node2 = heapq.heappop(heap)
            merged = HuffmanNode(node1.freq + node2.freq)
            merged.left = node1
            merged.right = node2
            heapq.heappush(heap, merged)
        return heap[0]

    def make_codes_helper(self, root, current_code):
        if root is None:
            return
        if root.char is not None:
            self.codes[root.char] = current_code
            self.reverse_mapping[current_code] = root.char
            return
        self.make_codes_helper(root.left, current_code + "0")
        self.make_codes_helper(root.right, current_code + "1")

    def make_codes(self, root):
        self.make_codes_helper(root, "")

    def get_encoded_text(self, text):
        encoded_text = ""
        for char in text:
            encoded_text += self.codes[char]
        return encoded_text

    def pad_encoded_text(self, encoded_text):
        extra_padding = 8 - len(encoded_text) % 8
        for i in range(extra_padding):
            encoded_text += "0"
        padded_info = "{0:08b}".format(extra_padding)
        encoded_text = padded_info + encoded_text
        return encoded_text

    def get_byte_array(self, padded_encoded_text):
        if len(padded_encoded_text) % 8 != 0:
            raise ValueError("Padded encoded text should be a multiple of 8 in length")
        b = bytearray()
        for i in range(0, len(padded_encoded_text), 8):
            byte = padded_encoded_text[i:i+8]
            b.append(int(byte, 2))
        return b

    def compress(self, text, file_path):
        freq_dict = self.make_frequency_dict(text)
        heap = self.make_heap(freq_dict)
        root = self.merge_nodes(heap)
        self.make_codes(root)
        encoded_text = self.get_encoded_text(text)
        padded_encoded_text = self.pad_encoded_text(encoded_text)
        byte_array = self.get_byte_array(padded_encoded_text)
        with open(file_path, 'wb') as output:
            output.write(bytes(byte_array))
        return file_path

class HuffmanGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("Huffman Compression - @BugRuster || @Cepheidloom")
        self.root.geometry("700x200")
        self.input_file_path = ""
        self.output_file_path = ""
        self.hc = HuffmanCoding()

        # Create input file selection widgets
        input_frame = tk.Frame(self.root)
        input_frame.pack(pady=10)

        input_label = tk.Label(input_frame, text="Select a file to compress:")
        input_label.pack(side=tk.LEFT, padx=10)

        self.input_file_entry = tk.Entry(input_frame, width=40)
        self.input_file_entry.pack(side=tk.LEFT, padx=10)

        browse_button = tk.Button(input_frame, text="Browse", command=self.browse_input_file)
        browse_button.pack(side=tk.LEFT, padx=10)

        # Create output file selection widgets
        output_frame = tk.Frame(self.root)
        output_frame.pack(pady=10)

        output_label = tk.Label(output_frame, text="Save compressed file as:")
        output_label.pack(side=tk.LEFT, padx=10)

        self.output_file_entry = tk.Entry(output_frame, width=40)
        self.output_file_entry.pack(side=tk.LEFT, padx=10)

        save_button = tk.Button(output_frame, text="Save", command=self.browse_output_file)
        save_button.pack(side=tk.LEFT, padx=10)

        # Create compress button
        compress_button = tk.Button(self.root, text="Compress File", command=self.compress_file)
        compress_button.pack(pady=10)

    def browse_input_file(self):
        self.input_file_path = filedialog.askopenfilename()
        self.input_file_entry.delete(0, tk.END)
        self.input_file_entry.insert(0, self.input_file_path)

    def browse_output_file(self):
        self.output_file_path = filedialog.asksaveasfilename(defaultextension=".bin")
        self.output_file_entry.delete(0, tk.END)
        self.output_file_entry.insert(0, self.output_file_path)

    def compress_file(self):
        if not self.input_file_path:
            tk.messagebox.showerror("Error", "Please select an input file")
            return
        if not self.output_file_path:
            tk.messagebox.showerror("Error", "Please select an output file")
            return
        try:
            with open(self.input_file_path, 'r') as f:
                text = f.read()
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to read input file: {str(e)}")
            return
        try:
            file_path = self.hc.compress(text, self.output_file_path)
            tk.messagebox.showinfo("Success", f"File compressed and saved to {file_path}")
        except Exception as e:
            tk.messagebox.showerror("Error", f"Failed to compress file: {str(e)}")

if __name__ == "__main__":
    root = tk.Tk()
    app = HuffmanGUI(root)
    root.mainloop()