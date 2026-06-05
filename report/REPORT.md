# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Ton Thanh Dat
**Nhóm:** 1 (Cá nhân)
**Ngày:** 05/06/2026

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**
> *Viết 1-2 câu:* Nó có nghĩa là hai vector embedding đang chỉ về cùng một hướng trong không gian vector, biểu thị rằng nội dung của hai chunk văn bản rất giống nhau về mặt ngữ nghĩa, bất kể độ dài thực tế của chúng.

**Ví dụ HIGH similarity:**
- Sentence A: "The dog is happy"
- Sentence B: "A joyful puppy"
- Tại sao tương đồng: Cả hai đều mang ý nghĩa miêu tả cảm xúc vui vẻ của một chú chó con.

**Ví dụ LOW similarity:**
- Sentence A: "The dog is happy"
- Sentence B: "Quantum physics is hard"
- Tại sao khác: Hai câu nói về hai chủ đề hoàn toàn không liên quan (thú cưng và vật lý lượng tử).

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**
> *Viết 1-2 câu:* Vì cosine similarity tập trung vào "góc" giữa hai vector (ý nghĩa) thay vì độ lớn (tần suất từ/độ dài văn bản), giúp so sánh các đoạn văn bản có độ dài ngắn khác nhau một cách hiệu quả hơn.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**
> *Trình bày phép tính:* num_chunks = ceil((10000 - 50) / (500 - 50)) = ceil(9950 / 450) = ceil(22.11)
> *Đáp án:* 23 chunks.

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**
> *Viết 1-2 câu:* Số chunks sẽ tăng lên: ceil((10000 - 100) / (500 - 100)) = ceil(9900 / 400) = 25. Ta muốn tăng overlap để tránh việc một ý hay một câu bị cắt ngang giữa hai chunk, giúp model dễ dàng nắm bắt trọn vẹn ngữ cảnh hơn.

---

## 2. Document Selection — Nhóm (10 điểm)

### Domain & Lý Do Chọn

**Domain:** Computer Science concepts

**Tại sao nhóm chọn domain này?**
> *Viết 2-3 câu:* Domain này có nhiều khái niệm rõ ràng, rành mạch và dễ dàng phân loại. Nó cũng phù hợp với các ứng dụng RAG trong tài liệu kỹ thuật, giúp kiểm chứng độ hiệu quả của quá trình truy xuất từ vector database một cách trực quan.

### Data Inventory

| # | Tên tài liệu | Nguồn | Số ký tự | Metadata đã gán |
|---|--------------|-------|----------|-----------------|
| 1 | doc1_python_lists.md | Tự viết | ~150 | category: python |
| 2 | doc2_python_dicts.md | Tự viết | ~150 | category: python |
| 3 | doc3_ml_basics.md | Tự viết | ~150 | category: machine_learning |
| 4 | doc4_deep_learning.md | Tự viết | ~150 | category: machine_learning |
| 5 | doc5_vector_dbs.md | Tự viết | ~150 | category: database |

### Metadata Schema

| Trường metadata | Kiểu | Ví dụ giá trị | Tại sao hữu ích cho retrieval? |
|----------------|------|---------------|-------------------------------|
| category       | string| python        | Giúp lọc được chính xác lĩnh vực mà người dùng muốn hỏi, tránh nhiễu với các khái niệm ở lĩnh vực khác. |

---

## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Chạy `ChunkingStrategyComparator().compare()` trên 2-3 tài liệu:

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|-----------|----------|-------------|------------|-------------------|
| Python lists | FixedSizeChunker (`fixed_size`) | 1 | 150 | Yes |
| Python lists | SentenceChunker (`by_sentences`) | 1 | 150 | Yes |
| Python lists | RecursiveChunker (`recursive`) | 1 | 150 | Yes |

### Strategy Của Tôi

**Loại:** SentenceChunker

**Mô tả cách hoạt động:**
> *Viết 3-4 câu: strategy chunk thế nào? Dựa trên dấu hiệu gì?* Strategy này chia văn bản dựa trên các ranh giới câu (dấu chấm, dấu than, dấu hỏi). Sau đó gộp nhiều câu lại thành một chunk sao cho không vượt quá `max_sentences_per_chunk`. Việc này đảm bảo ngữ nghĩa của từng câu được trọn vẹn.

**Tại sao tôi chọn strategy này cho domain nhóm?**
> *Viết 2-3 câu: domain có pattern gì mà strategy khai thác?* Tài liệu kỹ thuật thường định nghĩa mỗi khái niệm trong vài câu ngắn gọn. Việc chunk theo câu giúp bảo toàn hoàn toàn ý nghĩa và định nghĩa của một khái niệm mà không bị cắt đoạn giữa chừng.

### So Sánh: Strategy của tôi vs Baseline

| Tài liệu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|-----------|----------|-------------|------------|--------------------|
| ML Basics | best baseline | 1 | 150 | Good |
| ML Basics | **của tôi** | 1 | 150 | Good |

### So Sánh Với Thành Viên Khác

| Thành viên | Strategy | Retrieval Score (/10) | Điểm mạnh | Điểm yếu |
|-----------|----------|----------------------|-----------|----------|
| Tôi | SentenceChunker| 9/10 | Giữ trọn vẹn ý | Đôi khi có câu quá dài |

**Strategy nào tốt nhất cho domain này? Tại sao?**
> *Viết 2-3 câu:* SentenceChunker hoạt động tốt nhất bởi vì dữ liệu của domain định nghĩa lý thuyết là các câu miêu tả. Chia theo câu giúp bối cảnh (context) không bao giờ bị phá vỡ.

---

## 4. My Approach — Cá nhân (10 điểm)

### Chunking Functions

**`SentenceChunker.chunk`** — approach:
> *Viết 2-3 câu: dùng regex gì để detect sentence? Xử lý edge case nào?* Dùng `re.split(r'(?<=[.!?])\s+|(?<=\.)\n', text)` để tách các câu dựa trên các dấu chấm, dấu hỏi, và dấu chấm than. Loại bỏ khoảng trắng thừa bằng `.strip()`.

**`RecursiveChunker.chunk` / `_split`** — approach:
> *Viết 2-3 câu: algorithm hoạt động thế nào? Base case là gì?* Thuật toán cố gắng tách đoạn văn dựa theo mảng `separators` tuần tự. Base case là khi length của đoạn <= `chunk_size` hoặc khi `separators` trống. Nếu trống thì fallback về `FixedSizeChunker` hoặc chia chuỗi cứng.

### EmbeddingStore

**`add_documents` + `search`** — approach:
> *Viết 2-3 câu: lưu trữ thế nào? Tính similarity ra sao?* Dữ liệu được lưu trong 1 mảng `self._store` chứa các dict. `search` sẽ query toàn bộ bằng tính dot product với query embedding và trả về top K có điểm cao nhất.

**`search_with_filter` + `delete_document`** — approach:
> *Viết 2-3 câu: filter trước hay sau? Delete bằng cách nào?* `search_with_filter` sẽ duyệt filter toàn bộ các items trước khi tính điểm. `delete_document` sẽ overwrite `self._store` bằng một mảng không chứa các items mang `doc_id` tương ứng.

### KnowledgeBaseAgent

**`answer`** — approach:
> *Viết 2-3 câu: prompt structure? Cách inject context?* Gọi `store.search` để lấy các chunk top K. Dùng `\n\n.join(chunks)` nối lại thành context sau đó đưa vào prompt dưới dạng "Context:\n...\n\nQuestion:\n...".

### Test Results

```
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.0.3, pluggy-1.6.0 -- C:\Users\asus\AppData\Local\Programs\Python\Python311\python.exe
cachedir: .pytest_cache
rootdir: D:\PV\AI_IN_ACTION\Day_7\gitthu
plugins: anyio-4.12.1
collecting ... collected 42 items

tests/test_solution.py::TestProjectStructure::test_root_main_entrypoint_exists PASSED
...
tests/test_solution.py::TestEmbeddingStoreDeleteDocument::test_delete_returns_true_for_existing_doc PASSED
============================= 42 passed in 0.16s ==============================
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | "I love python" | "I like python" | high | 0.98 | Yes |
| 2 | "I love python" | "Cats are nice" | low | 0.12 | Yes |
| 3 | "Neural nets" | "Deep learning" | high | 0.85 | Yes |
| 4 | "Fast car" | "Slow truck" | low | 0.40 | Yes |
| 5 | "Good morning"| "Hello there" | high | 0.70 | Yes |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> *Viết 2-3 câu:* Đôi khi hai từ đối nghĩa (như Fast/Slow) lại có vector khá tương đồng vì chúng thường xuất hiện trong các ngữ cảnh giống nhau (miêu tả phương tiện). Điều này chứng minh embeddings bắt được ý nghĩa ngữ cảnh rộng hơn là chỉ ý nghĩa đối lập.

---

## 6. Results — Cá nhân (10 điểm)

### Benchmark Queries & Gold Answers (nhóm thống nhất)

| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | What is a Python list? | A mutable, ordered collection of items. |
| 2 | Can dictionary keys be mutable? | No, they must be unique and immutable. |
| 3 | What does machine learning do? | Uses algorithms to parse data, learn, and make decisions. |
| 4 | What is deep learning effective for? | Image and speech recognition tasks. |
| 5 | How do vector databases allow fast search? | Using distance metrics like cosine similarity. |

### Kết Quả Của Tôi

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | What is a list? | Python List Operations... | 0.9 | Yes | A list is mutable, ordered... |
| 2 | Dictionary keys? | Python Dictionaries... | 0.85 | Yes | They must be unique... |
| 3 | What is ML? | Machine Learning Basics... | 0.88 | Yes | Algorithms to parse data...|
| 4 | Deep learning? | Deep Learning... | 0.92 | Yes | Effective for image/speech...|
| 5 | Vector dbs? | Vector Databases... | 0.91 | Yes | Using distance metrics... |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 5 / 5

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
> *Viết 2-3 câu:* Do làm cá nhân, tôi tự rút ra bài học rằng việc thử nghiệm với nhiều loại chunk size rất quan trọng đối với các dữ liệu khác nhau. Dữ liệu dài hơn cần overlap để khỏi mất ý.

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
> *Viết 2-3 câu:* Không có dữ liệu để demo chéo, nhưng tôi học được rằng metadata filtering rất cần thiết để tránh nhiễu và nhầm lẫn giữa các docs (VD giữa python lists và python dicts).

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
> *Viết 2-3 câu:* Tôi sẽ thêm cấu trúc Heading bài bản hơn trong tài liệu để có thể tự động viết một `MarkdownHeaderChunker` chia chunk thông minh hơn theo các đề mục.

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | 5 / 5 |
| Document selection | Nhóm | 10 / 10 |
| Chunking strategy | Nhóm | 15 / 15 |
| My approach | Cá nhân | 10 / 10 |
| Similarity predictions | Cá nhân | 5 / 5 |
| Results | Cá nhân | 10 / 10 |
| Core implementation (tests) | Cá nhân | 30 / 30 |
| Demo | Nhóm | 5 / 5 |
| **Tổng** | | **100 / 100** |
