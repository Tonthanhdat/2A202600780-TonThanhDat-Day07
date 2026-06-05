import os
import re
import math
from src.chunking import RecursiveChunker
from src.store import EmbeddingStore
from src.agent import KnowledgeBaseAgent

class SimpleTFIDFEmbedder:
    def __init__(self):
        self.vocab = {}
        self.idf = {}
        self.doc_count = 0
        
    def fit(self, texts):
        self.doc_count = len(texts)
        df = {}
        for text in texts:
            words = set(re.findall(r'\w+', text.lower()))
            for w in words:
                df[w] = df.get(w, 0) + 1
        
        for w, count in df.items():
            self.idf[w] = math.log(self.doc_count / (1 + count))
            
        self.vocab = {w: i for i, w in enumerate(self.idf.keys())}
        
    def embed(self, text):
        words = re.findall(r'\w+', text.lower())
        tf = {}
        for w in words:
            tf[w] = tf.get(w, 0) + 1
            
        vec = [0.0] * len(self.vocab)
        for w, count in tf.items():
            if w in self.vocab:
                vec[self.vocab[w]] = count * self.idf[w]
                
        # Normalize
        norm = math.sqrt(sum(v*v for v in vec))
        if norm > 0:
            vec = [v/norm for v in vec]
        return vec

import sys
sys.stdout.reconfigure(encoding='utf-8')

def main():
    files = ["100152.txt", "118633.txt", "103191.txt"]
    chunker = RecursiveChunker(chunk_size=500)
    
    all_chunks = []
    for f in files:
        with open(os.path.join("data/bocongan", f), "r", encoding="utf-8") as file:
            text = file.read()
            chunks = chunker.chunk(text)
            for i, c in enumerate(chunks):
                all_chunks.append({"text": c, "metadata": {"source": f, "doc_id": f"{f}_{i}"}})
                
    embedder = SimpleTFIDFEmbedder()
    embedder.fit([c["text"] for c in all_chunks] + [
        "Theo Thông tư liên tịch về tội chứa chấp hoặc tiêu thụ tài sản do người khác phạm tội mà có, thế nào là tài sản/vật phạm pháp có giá trị lớn, rất lớn, đặc biệt lớn?",
        "Hồ sơ đề nghị cấp, sửa đổi, bổ sung hộ chiếu phổ thông gồm những giấy tờ gì? Yêu cầu ảnh như thế nào?",
        "Chỉ tìm trong văn bản còn hiệu lực năm 2016: thời hạn giải quyết hồ sơ hộ chiếu tại Phòng Quản lý xuất nhập cảnh và tại Cục Quản lý xuất nhập cảnh là bao lâu?",
        "Nếu bị mất hộ chiếu, người dân phải trình báo trong thời hạn bao lâu và cần xuất trình giấy tờ gì? Nếu gửi đơn qua bưu điện thì cần điều kiện gì?",
        "Trong văn bản ban hành tiêu chuẩn quốc gia lĩnh vực an ninh, có bao nhiêu tiêu chuẩn được ban hành? Mã tiêu chuẩn của “Quy trình giám định ADN” và “Quy trình giám định dữ liệu số trong các thiết bị kết nối với máy vi tính” là gì?"
    ])
    
    from src.models import Document
    store = EmbeddingStore(embedding_fn=embedder.embed)
    docs_to_add = [Document(id=c["metadata"]["doc_id"], content=c["text"], metadata=c["metadata"]) for c in all_chunks]
    store.add_documents(docs_to_add)
    
    queries = [
        "Theo Thông tư liên tịch về tội chứa chấp hoặc tiêu thụ tài sản do người khác phạm tội mà có, thế nào là tài sản/vật phạm pháp có giá trị lớn, rất lớn, đặc biệt lớn?",
        "Hồ sơ đề nghị cấp, sửa đổi, bổ sung hộ chiếu phổ thông gồm những giấy tờ gì? Yêu cầu ảnh như thế nào?",
        "Chỉ tìm trong văn bản còn hiệu lực năm 2016: thời hạn giải quyết hồ sơ hộ chiếu tại Phòng Quản lý xuất nhập cảnh và tại Cục Quản lý xuất nhập cảnh là bao lâu?",
        "Nếu bị mất hộ chiếu, người dân phải trình báo trong thời hạn bao lâu và cần xuất trình giấy tờ gì? Nếu gửi đơn qua bưu điện thì cần điều kiện gì?",
        "Trong văn bản ban hành tiêu chuẩn quốc gia lĩnh vực an ninh, có bao nhiêu tiêu chuẩn được ban hành? Mã tiêu chuẩn của “Quy trình giám định ADN” và “Quy trình giám định dữ liệu số trong các thiết bị kết nối với máy vi tính” là gì?"
    ]
    
    for i, q in enumerate(queries):
        results = store.search(q, top_k=3)
        print(f"\n=== Query {i+1} ===")
        for r in results:
            print(f"Score: {r['score']:.4f} | Source: {r['metadata']['source']}")
            print(f"Content: {r['content']}")

if __name__ == "__main__":
    main()
