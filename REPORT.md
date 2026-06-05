# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Tùng Mai
**Nhóm:** [Tên nhóm]
**Ngày:** 05/06/2026

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**

High cosine similarity cho thấy hai vector embedding có hướng gần giống nhau trong không gian vector. Điều này thường biểu thị hai câu hoặc hai đoạn văn có nội dung và ý nghĩa tương đồng.

**Ví dụ HIGH similarity:**

* Sentence A: Python is a popular programming language.
* Sentence B: Python is widely used for software development.
* Tại sao tương đồng: Cả hai câu đều nói về Python và việc sử dụng Python trong lập trình.

**Ví dụ LOW similarity:**

* Sentence A: Python is a programming language.
* Sentence B: The weather is rainy today.
* Tại sao khác: Hai câu thuộc hai chủ đề hoàn toàn khác nhau.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**

Cosine similarity tập trung vào hướng của vector thay vì độ lớn của vector. Trong embedding, hướng thường phản ánh ý nghĩa ngữ nghĩa tốt hơn khoảng cách Euclidean.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**

Bước nhảy:

500 - 50 = 450

Số chunk:

ceil((10000 - 500) / 450) + 1

= ceil(9500 / 450) + 1

= 22 + 1

= 23

**Đáp án:** 23 chunks

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**

Overlap tăng làm bước nhảy giảm nên số lượng chunk tăng lên. Overlap lớn giúp giữ được ngữ cảnh giữa các chunk và giảm nguy cơ mất thông tin khi câu hoặc đoạn văn bị cắt ở ranh giới chunk.

---

## 4. My Approach — Cá nhân (10 điểm)

### Chunking Functions

**SentenceChunker.chunk — approach**

Em sử dụng biểu thức chính quy để tách văn bản theo các dấu kết thúc câu như ".", "!" và "?". Sau khi tách, các câu được gom thành từng nhóm với số lượng tối đa bằng `max_sentences_per_chunk`.

**RecursiveChunker.chunk / _split — approach**

Thuật toán thực hiện chia văn bản theo thứ tự ưu tiên của các separator như đoạn văn, dòng, câu và khoảng trắng. Nếu một phần vẫn vượt quá `chunk_size`, hàm tiếp tục gọi đệ quy với separator tiếp theo cho đến khi kích thước phù hợp hoặc phải cắt theo ký tự.

### EmbeddingStore

**add_documents + search — approach**

Mỗi document được chuyển thành embedding thông qua embedding function rồi lưu cùng metadata trong vector store. Khi tìm kiếm, query được embed và độ tương đồng được tính bằng phép nhân vô hướng giữa embedding của query và embedding của từng document.

**search_with_filter + delete_document — approach**

`search_with_filter` lọc trước theo metadata rồi mới thực hiện tìm kiếm tương đồng trên tập kết quả đã lọc. `delete_document` loại bỏ toàn bộ record có `doc_id` tương ứng khỏi vector store.

### KnowledgeBaseAgent

**answer — approach**

Agent truy xuất top-k document liên quan từ vector store, ghép các document này thành context rồi chèn vào prompt cùng câu hỏi của người dùng. Prompt hoàn chỉnh được gửi cho LLM để sinh câu trả lời theo mô hình RAG.

### Test Results

```bash
pytest tests/ -v
```

Kết quả:

* Tổng số test: 42
* Số test pass: 42
* Số test fail: 0

**Số tests pass:** 42 / 42



## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | | | high / low | | |
| 2 | | | high / low | | |
| 3 | | | high / low | | |
| 4 | | | high / low | | |
| 5 | | | high / low | | |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> *Viết 2-3 câu:*

---

## 6. Results — Cá nhân (10 điểm)

Chạy 5 benchmark queries của nhóm trên implementation cá nhân của bạn trong package `src`. **5 queries phải trùng với các thành viên cùng nhóm.**

### Benchmark Queries & Gold Answers (nhóm thống nhất)

| # | Query                                                                                   | Gold Answer                                                                                                         |
| - | --------------------------------------------------------------------------------------- | ------------------------------------------------------------------------------------------------------------------- |
| 1 | Thẩm quyền ban hành văn bản quy phạm pháp luật thuộc những cơ quan nào?                 | Quốc hội, Chính phủ, Bộ trưởng, UBND, HĐND và các cơ quan có thẩm quyền theo Luật Ban hành VBQPPL.                  |
| 2 | Người dân có quyền khiếu nại quyết định hành chính trong trường hợp nào?                | Khi cho rằng quyết định hành chính hoặc hành vi hành chính xâm phạm quyền và lợi ích hợp pháp của mình.             |
| 3 | Điều kiện để đăng ký kết hôn hợp pháp tại Việt Nam là gì?                               | Nam đủ 20 tuổi, nữ đủ 18 tuổi, tự nguyện kết hôn, không thuộc trường hợp cấm kết hôn.                               |
| 4 | Hành vi điều khiển phương tiện giao thông sau khi sử dụng rượu bia có bị xử phạt không? | Có. Người điều khiển phương tiện có nồng độ cồn vượt mức cho phép sẽ bị xử phạt theo quy định pháp luật giao thông. |
| 5 | Người sử dụng đất có những quyền cơ bản nào theo Luật Đất đai?                          | Quyền sử dụng, chuyển nhượng, cho thuê, thừa kế, tặng cho, thế chấp và các quyền khác theo quy định pháp luật.      |

### Kết Quả Của Tôi

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | | | | | |
| 2 | | | | | |
| 3 | | | | | |
| 4 | | | | | |
| 5 | | | | | |

**Bao nhiêu queries trả về chunk relevant trong top-3?** __ / 5

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
> *Viết 2-3 câu:*

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
> *Viết 2-3 câu:*

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
> *Viết 2-3 câu:*

---

## Tự Đánh Giá

| Tiêu chí | Loại | Điểm tự đánh giá |
|----------|------|-------------------|
| Warm-up | Cá nhân | / 5 |
| Document selection | Nhóm | / 10 |
| Chunking strategy | Nhóm | / 15 |
| My approach | Cá nhân | / 10 |
| Similarity predictions | Cá nhân | / 5 |
| Results | Cá nhân | / 10 |
| Core implementation (tests) | Cá nhân | / 30 |
| Demo | Nhóm | / 5 |
| **Tổng** | | **/ 100** |







## Part 3 — So Sánh Retrieval Strategy (Nhóm)

### Exercise 3.0 — Chuẩn Bị Tài Liệu

**Domain:** Hệ thống văn bản pháp luật Việt Nam

### Data Inventory

| #  | Tên tài liệu                           | Nguồn | Số ký tự  | Metadata đã gán    |
| -- | -------------------------------------- | ----- | --------- | ------------------ |
| 1  | Văn bản Bộ Tư pháp                     | VBPL  | ~100.000+ | slug, dvid, source |
| 2  | Văn bản Bộ Công an                     | VBPL  | ~100.000+ | slug, dvid, source |
| 3  | Văn bản Bộ Giáo dục và Đào tạo         | VBPL  | ~100.000+ | slug, dvid, source |
| 4  | Văn bản Bộ Tài chính                   | VBPL  | ~100.000+ | slug, dvid, source |
| 5  | Văn bản Bộ Y tế                        | VBPL  | ~100.000+ | slug, dvid, source |
| 6  | Văn bản Bộ Giao thông Vận tải          | VBPL  | ~100.000+ | slug, dvid, source |
| 7  | Văn bản Ngân hàng Nhà nước             | VBPL  | ~100.000+ | slug, dvid, source |
| 8  | Văn bản Tòa án nhân dân tối cao        | VBPL  | ~100.000+ | slug, dvid, source |
| 9  | Văn bản Viện kiểm sát nhân dân tối cao | VBPL  | ~100.000+ | slug, dvid, source |
| 10 | Văn bản Văn phòng Chính phủ            | VBPL  | ~100.000+ | slug, dvid, source |

### Metadata Schema

| Trường metadata | Kiểu   | Ví dụ                        |
| --------------- | ------ | ---------------------------- |
| slug            | string | botuphap                     |
| dvid            | string | 41                           |
| source          | string | vbpl.vn                      |
| search_url      | string | https://vbpl.vn/botuphap/... |

### Mô tả dữ liệu

Nhóm sử dụng dữ liệu được thu thập từ hệ thống Văn bản Pháp luật Việt Nam (VBPL). Bộ dữ liệu bao gồm các văn bản pháp luật được ban hành bởi nhiều cơ quan nhà nước khác nhau như Bộ Tư pháp, Bộ Công an, Bộ Giáo dục và Đào tạo, Bộ Tài chính, Bộ Y tế, Ngân hàng Nhà nước, Tòa án nhân dân tối cao và nhiều đơn vị khác.

Metadata được lưu cùng mỗi văn bản nhằm hỗ trợ retrieval theo nguồn ban hành. Điều này giúp hệ thống có thể lọc và truy xuất chính xác hơn khi người dùng đặt câu hỏi liên quan đến một lĩnh vực pháp luật cụ thể.
