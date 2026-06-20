import os

class ChunkService:

    def __init__(self):
        self.chunk_size = int(os.getenv("CHUNK_SIZE"))
        self.overlap = int(os.getenv("CHUNK_OVERLAP"))
        
        if self.chunk_size <= 0:
            raise ValueError("chunk_size must be greater than 0.")
        if self.overlap <= 0:
            raise ValueError("overlap must be greater than 0.")
        if self.overlap >= self.chunk_size:
            raise ValueError("chunk_size must be greater than overlap.")


    def chunk_by_char(self, text: str) -> list[str]:
        chunks = []
        start = 0

        while start < len(text):
            end = start + self.chunk_size

            try:
                # reset end to full word
                if text[end] != " " and text[end+1] != " ":
                    while text[end] != " ":
                        end -= 1
            except IndexError:
                pass
        
            chunk = text[start:end].strip()
            if len(chunk) > self.overlap:
                chunks.append(chunk)

            start += (self.chunk_size - self.overlap)

            try:
                # reset start to full word
                if text[start] != " " and text[start-1] != " ":
                    while text[start] != " ":
                        start -= 1
            except IndexError:
                pass

        return chunks
    

    def chunk_by_paragraph(self, text: str) -> list[str]:
        paragraphs = [p.strip() for p in text.split("\n\n") if len(p) > 0]
        chunks = []

        for paragraph in paragraphs:
            if len(paragraph) < self.chunk_size:
                chunks.append(paragraph)
            else:
                chunks += self.chunk_by_char(paragraph)
        
        return chunks
