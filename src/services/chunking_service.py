
class ChunkService:

    def __init__(self, chunk_size, overlap):
        self.chunk_size = chunk_size
        self.overlap = overlap
        
        if chunk_size <= 0:
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
        
            chunk = text[start:end].strip()
            if len(chunk) > 0:
                chunks.append(chunk)

            start += (self.chunk_size - self.overlap)

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
