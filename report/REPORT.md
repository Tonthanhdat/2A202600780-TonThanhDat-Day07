# Báo Cáo Lab 7: Embedding & Vector Store

**Họ tên:** Tôn Thành Đạt
**Nhóm:** UET
**Ngày:** 05/06/2026

---

## 1. Warm-up (5 điểm)

### Cosine Similarity (Ex 1.1)

**High cosine similarity nghĩa là gì?**

Hai đoạn văn bản có high cosine similarity nghĩa là vector biểu diễn của chúng có hướng rất gần nhau trong không gian nhiều chiều, cho thấy nội dung hoặc ý nghĩa ngữ nghĩa của chúng rất tương đồng.

**Ví dụ HIGH similarity:**

* Sentence A: Mèo là loài động vật rất thích bắt chuột.
* Sentence B: Những chú mèo thường có sở thích săn bắt chuột.
* Tại sao tương đồng: Cùng diễn đạt một ý nghĩa về tập tính của loài mèo, dù dùng từ vựng hơi khác nhau.

**Ví dụ LOW similarity:**

* Sentence A: Mèo là loài động vật rất thích bắt chuột.
* Sentence B: Lãi suất ngân hàng năm nay tăng mạnh do lạm phát.
* Tại sao khác: Hai câu thuộc hai lĩnh vực hoàn toàn khác nhau (động vật học và kinh tế học), không chia sẻ ý nghĩa chung nào.

**Tại sao cosine similarity được ưu tiên hơn Euclidean distance cho text embeddings?**

Cosine similarity chỉ quan tâm đến góc (hướng) giữa hai vector chứ không phụ thuộc vào độ lớn (magnitude) của vector. Điều này rất phù hợp với text vì độ dài của câu không làm ảnh hưởng đến việc đánh giá độ tương đồng về mặt ngữ nghĩa.

### Chunking Math (Ex 1.2)

**Document 10,000 ký tự, chunk_size=500, overlap=50. Bao nhiêu chunks?**

Bước nhảy: 500 - 50 = 450
Số chunk: ceil((10,000 - 500) / 450) + 1 = ceil(9500 / 450) + 1 = 22.11 (làm tròn lên 23)

**Đáp án:** 23 chunks

**Nếu overlap tăng lên 100, chunk count thay đổi thế nào? Tại sao muốn overlap nhiều hơn?**

Nếu overlap tăng lên 100, mẫu số sẽ giảm (500 - 100 = 400), dẫn đến số chunks tăng lên (ceil(9900/400) = 25 chunks). Ta muốn overlap nhiều hơn để tránh việc cắt đứt các câu hoặc đoạn mang ý nghĩa quan trọng ở giữa chừng, giúp bảo toàn ngữ cảnh chuyển tiếp giữa các chunk.

---

## 2. Document Selection — Nhóm (10 điểm)


**Domain:** Hệ thống văn bản pháp luật Việt Nam

**Tại sao nhóm chọn domain này?**

Lý do nhóm chọn domain này là vì hệ thống văn bản pháp luật Việt Nam có cấu trúc rõ ràng, đa dạng về thể loại và chứa nhiều thông tin hữu ích để thử nghiệm các kỹ thuật retrieval và chunking khác nhau. Ngoài ra, dữ liệu này cũng giúp ích cho việc xây dựng các trợ lý pháp luật và các ứng dụng liên quan đến pháp luật.

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


## 3. Chunking Strategy — Cá nhân chọn, nhóm so sánh (15 điểm)

### Baseline Analysis

Chạy `ChunkingStrategyComparator().compare()` trên 2 tài liệu pháp luật (chunk_size=500):

| Tài liệu | Strategy | Chunk Count | Avg Length | Preserves Context? |
|-----------|----------|-------------|------------|-------------------|
| 100152.txt | FixedSizeChunker (`fixed_size`) | 23 | 487.17 | Kém (có thể cắt đứt ngang câu chữ) |
| 100152.txt | SentenceChunker (`by_sentences`) | 23 | 467.09 | Khá (giữ nguyên được câu hoàn chỉnh) |
| 100152.txt | RecursiveChunker (`recursive`) | 29 | 370.17 | Tốt (bảo toàn cấu trúc đoạn/điều luật) |
| 118633.txt | FixedSizeChunker (`fixed_size`) | 32 | 488.34 | Kém |
| 118633.txt | SentenceChunker (`by_sentences`) | 30 | 499.23 | Khá |
| 118633.txt | RecursiveChunker (`recursive`) | 38 | 393.92 | Tốt |

### Strategy Của Tôi

**Loại:** RecursiveChunker

**Mô tả cách hoạt động:**
Thuật toán chia văn bản theo thứ tự ưu tiên của các dấu phân cách (như đoạn văn kép `\n\n`, dấu xuống dòng `\n`, dấu chấm câu và khoảng trắng). Nếu một phần văn bản bị cắt vẫn vượt quá kích thước cho phép, thuật toán sẽ gọi đệ quy để tiếp tục cắt phần đó bằng dấu phân cách ở cấp độ thấp hơn.

**Tại sao tôi chọn strategy này cho domain nhóm?**
Domain nhóm là "Hệ thống văn bản pháp luật Việt Nam", đặc thù có cấu trúc hình thức rất chặt chẽ (Điều, Khoản, Điểm) phân tách rõ ràng bằng các dấu xuống dòng kép hoặc đơn. `RecursiveChunker` sẽ ưu tiên cắt theo cấu trúc văn bản tự nhiên này trước, giúp bảo toàn toàn vẹn nội dung pháp lý của một Khoản/Điểm hơn so với việc cắt ngang ký tự hoặc chỉ tách câu đơn thuần.

### So Sánh: Strategy của tôi vs Baseline

| Tài liệu | Strategy | Chunk Count | Avg Length | Retrieval Quality? |
|-----------|----------|-------------|------------|--------------------|
| 100152.txt | best baseline (SentenceChunker) | 23 | 467.09 | Tạm ổn, nhưng đôi khi ghép nhầm các câu không liên quan. |
| 100152.txt | **của tôi (RecursiveChunker)** | 29 | 370.17 | Tốt, trả về đúng các Khoản/Điểm của luật để agent dễ đọc. |

## So Sánh Với Thành Viên Khác

| Thành viên | Strategy         | Retrieval Score (/10) | Điểm mạnh                                                                                    | Điểm yếu                                                                                        |
| ---------- | ---------------- | --------------------- | -------------------------------------------------------------------------------------------- | ----------------------------------------------------------------------------------------------- |
| Tùng       | FixedSizeChunker | 4.0                   | Dễ triển khai, tốc độ xử lý nhanh, kích thước chunk đồng đều                                 | Dễ cắt giữa điều luật hoặc khoản luật, làm mất ngữ cảnh pháp lý và giảm chất lượng retrieval    |
| Huy        | SentenceChunker  | 6.0                   | Giữ nguyên cấu trúc câu, nội dung dễ đọc và dễ hiểu hơn FixedSizeChunker                     | Một điều luật dài có thể bị chia thành nhiều câu riêng biệt, làm mất mối liên hệ giữa các khoản |
| Dương      | RecursiveChunker | 8.0                   | Cân bằng tốt giữa độ dài chunk và ngữ cảnh, hạn chế việc cắt nội dung ở vị trí không phù hợp | Chưa tận dụng được cấu trúc đặc thù của văn bản pháp luật như Chương, Điều, Khoản               |
| Đạt        | RecursiveChunker | 8.5                   | Giữ được nhiều ngữ cảnh hơn SentenceChunker, linh hoạt với các văn bản có độ dài khác nhau   | Chất lượng phụ thuộc nhiều vào tham số chunk size và chunk overlap                              |

### Strategy nào tốt nhất cho domain này? Tại sao?

Trong các strategy được so sánh, RecursiveChunker cho kết quả tốt nhất vì duy trì được ngữ cảnh của văn bản trong khi vẫn kiểm soát được độ dài của từng chunk. Đối với các tài liệu pháp luật có cấu trúc phức tạp và nhiều điều khoản dài, RecursiveChunker giúp cải thiện chất lượng retrieval đáng kể so với FixedSizeChunker và SentenceChunker. Tuy nhiên, một chiến lược chunking chuyên biệt theo cấu trúc pháp luật (Chương → Điều → Khoản) vẫn là hướng tiếp cận tối ưu nhất cho hệ thống RAG pháp lý.


---

## 4. My Approach — Cá nhân (10 điểm)

Giải thích cách tiếp cận của bạn khi implement các phần chính trong package `src`.

### Chunking Functions

**SentenceChunker.chunk — approach**

Sử dụng Regex `(?<=[.!?])\s+|(?<=\.)\n` kết hợp look-behind để tách câu chính xác mà không làm mất đi các dấu câu kết thúc (., !, ?). Nhóm các câu thành các đoạn chunk bằng cách lặp qua mảng câu và ghép chúng lại theo kích thước `max_sentences_per_chunk`.

**RecursiveChunker.chunk / _split — approach**

Thuật toán hoạt động theo cách đệ quy: thử cắt văn bản bằng dấu phân cách (separator) hiện tại, nếu có đoạn nào vượt quá `chunk_size` thì gọi đệ quy để tiếp tục cắt đoạn đó bằng separator ưu tiên kế tiếp. Base case là khi đoạn văn bản nhỏ hơn `chunk_size` hoặc khi đã duyệt qua hết danh sách separator.

### EmbeddingStore

**add_documents + search — approach**

Hỗ trợ hai chế độ: in-memory (`list[dict]`) và ChromaDB. Khi search ở in-memory, dùng vector truy vấn nhân vô hướng (`dot product`) với vector của từng đoạn lưu trữ, sau đó sắp xếp giảm dần theo điểm số để lấy top_k.

**search_with_filter + delete_document — approach**

Lọc (filter) siêu dữ liệu trước để giới hạn danh sách ứng viên, rồi mới gọi search giúp tăng tốc độ xử lý. Khi xóa (delete_document), kiểm tra cả ID của document và `metadata['doc_id']` để lọc bỏ hoàn toàn các chunk tương ứng khỏi bộ nhớ in-memory hoặc Chroma collection.

### KnowledgeBaseAgent

**answer — approach**

Gọi `search` để lấy top_k văn bản liên quan. Sau đó ghép nội dung text của chúng lại, inject vào phần `Context:` trong Prompt mẫu (có hướng dẫn rõ ràng yêu cầu trợ lý trả lời dựa trên context), rồi truyền toàn bộ cho LLM function sinh đáp án.

### Test Results

```text
============================= test session starts =============================
platform win32 -- Python 3.11.9, pytest-9.0.3, pluggy-1.6.0
collected 42 items

tests/test_solution.py::... [100%]

============================= 42 passed in 0.06s ==============================
```

**Số tests pass:** 42 / 42

---

## 5. Similarity Predictions — Cá nhân (5 điểm)

| Pair | Sentence A | Sentence B | Dự đoán | Actual Score | Đúng? |
|------|-----------|-----------|---------|--------------|-------|
| 1 | I love eating apples | My favorite fruit is apple | high | 0.85 | Có |
| 2 | I love eating apples | The car is driving fast | low | 0.12 | Có |
| 3 | Bank of the river | Bank interest rates are high | low | 0.35 | Có |
| 4 | The weather is cold | It is freezing outside | high | 0.81 | Có |
| 5 | AI is transforming tech | Tech is being changed by AI | high | 0.95 | Có |

**Kết quả nào bất ngờ nhất? Điều này nói gì về cách embeddings biểu diễn nghĩa?**
> *Viết 2-3 câu:* Bất ngờ nhất là cặp số 3 (Bank of the river vs Bank interest rate) có điểm thấp dù lặp lại từ "Bank". Điều này cho thấy embedding model hiện đại (dựa trên Transformer) thực sự hiểu được ngữ cảnh của từ thay vì chỉ so sánh mặt chữ, biểu diễn thành công tính đa nghĩa của từ vựng.

---

## 6. Results — Cá nhân (10 điểm)

Chạy 5 benchmark queries của nhóm trên implementation cá nhân của bạn trong package `src`. **5 queries phải trùng với các thành viên cùng nhóm.**

### Benchmark Queries & Gold Answers (nhóm thống nhất)

| # | Query | Gold Answer |
|---|-------|-------------|
| 1 | Theo Thông tư liên tịch về tội chứa chấp hoặc tiêu thụ tài sản do người khác phạm tội mà có, thế nào là tài sản/vật phạm pháp có giá trị lớn, rất lớn, đặc biệt lớn? | Giá trị lớn: từ 50 triệu đến dưới 200 triệu đồng. Rất lớn: từ 200 triệu đến dưới 500 triệu đồng. Đặc biệt lớn: từ 500 triệu đồng trở lên. Nguồn: data/bocongan/100152.txt, Điều 2, khoản 4-6. |
| 2 | Hồ sơ đề nghị cấp, sửa đổi, bổ sung hộ chiếu phổ thông gồm những giấy tờ gì? Yêu cầu ảnh như thế nào? | Hồ sơ gồm: 01 tờ khai mẫu X01; 02 ảnh mới chụp cỡ 4cm x 6cm, mặt nhìn thẳng, đầu để trần, không đeo kính màu, phông nền trắng. Trẻ em dưới 09 tuổi cấp chung hộ chiếu với cha hoặc mẹ thì nộp 02 ảnh cỡ 3cm x 4cm. Trẻ em dưới 14 tuổi nộp thêm bản sao hoặc bản chụp có chứng thực giấy khai sinh, nếu không chứng thực thì xuất trình bản chính để đối chiếu. Nguồn: data/bocongan/118633.txt, Điều 6. |
| 3 | Chỉ tìm trong văn bản còn hiệu lực năm 2016: thời hạn giải quyết hồ sơ hộ chiếu tại Phòng Quản lý xuất nhập cảnh và tại Cục Quản lý xuất nhập cảnh là bao lâu? | Với hồ sơ nộp tại Phòng Quản lý xuất nhập cảnh: không quá 08 ngày làm việc kể từ ngày nhận đủ hồ sơ hợp lệ. Với hồ sơ nộp tại Cục Quản lý xuất nhập cảnh: không quá 05 ngày làm việc. Trường hợp cần hộ chiếu gấp thì giải quyết sớm nhất trong thời hạn quy định. Nguồn: data/bocongan/118633.txt, Điều 8. Nên chạy filter metadata: status = Còn hiệu lực, filter_year = 2016. |
| 4 | Nếu bị mất hộ chiếu, người dân phải trình báo trong thời hạn bao lâu và cần xuất trình giấy tờ gì? Nếu gửi đơn qua bưu điện thì cần điều kiện gì? | Trong 48 giờ kể từ khi phát hiện mất hộ chiếu, người bị mất phải trình báo với cơ quan Quản lý xuất nhập cảnh nơi gần nhất theo mẫu X08 để hủy giá trị sử dụng của hộ chiếu đã mất. Khi trình báo cần xuất trình CMND hoặc thẻ CCCD còn giá trị. Nếu gửi đơn qua bưu điện thì đơn phải có xác nhận của Trưởng Công an phường, xã, thị trấn nơi người đó thường trú hoặc tạm trú. Nguồn: data/bocongan/118633.txt, Điều 9. |
| 5 | Trong văn bản ban hành tiêu chuẩn quốc gia lĩnh vực an ninh, có bao nhiêu tiêu chuẩn được ban hành? Mã tiêu chuẩn của “Quy trình giám định ADN” và “Quy trình giám định dữ liệu số trong các thiết bị kết nối với máy vi tính” là gì? | Văn bản ban hành 27 tiêu chuẩn quốc gia trong lĩnh vực an ninh. “Quy trình giám định ADN” có mã TCVN - AN: 035:2013. “Quy trình giám định dữ liệu số trong các thiết bị kết nối với máy vi tính” có mã TCVN - AN: 041:2013. Nguồn: data/bocongan/103191.txt, Điều 1. |

### Kết Quả Của Tôi

| # | Query | Top-1 Retrieved Chunk (tóm tắt) | Score | Relevant? | Agent Answer (tóm tắt) |
|---|-------|--------------------------------|-------|-----------|------------------------|
| 1 | Theo Thông tư liên tịch về tội chứa chấp... | 5. “Tài sản, vật phạm pháp có giá trị rất lớn” quy định tại điểm a khoản 3 Điều 250 Bộ luật Hình sự là tài sản, vật phạm pháp có giá trị từ hai trăm t... | 0.4496 | Có | Tài sản, vật phạm pháp có giá trị lớn là từ 50 triệu đến dưới 200 triệu đồng. Giá trị rất lớn là từ 200 triệu đến dưới 500 triệu đồng. Đặc biệt lớn là từ 500 triệu đồng trở lên. |
| 2 | Hồ sơ đề nghị cấp, sửa đổi... | 2. Người đề nghị cấp, sửa đổi, bổ sung hộ chiếu có thể nhận kết quả tại địa chỉ đã đăng ký với doanh nghiệp bưu chính. Điều 6. Về hồ sơ đề nghị cấp, sửa đổi, bổ sung hộ chiếu 1. Hồ sơ gồm: a) 01 tờ khai Mẫu X01; b) 02 ảnh mới chụp, cỡ 4cm x 6cm, mặt nhìn thẳng, đầu để trần, không đeo kính màu, phông nền màu trắng. Trẻ em dưới 09 tuổi cấp chung hộ chiếu với cha hoặc mẹ thì nộp 02 ảnh cỡ 3cm x 4cm; | 0.2070 | Có | Hồ sơ đề nghị cấp, sửa đổi, bổ sung hộ chiếu phổ thông gồm: 01 tờ khai Mẫu X01; 02 ảnh mới chụp, cỡ 4cm x 6cm, mặt nhìn thẳng, đầu để trần, không đeo kính màu, phông nền màu trắng. Trẻ em dưới 09 tuổi cấp chung hộ chiếu với cha hoặc mẹ thì nộp 02 ảnh cỡ 3cm x 4cm. |
| 3 | Chỉ tìm trong văn bản còn hiệu lực năm 2016... | 1. Đối với hồ sơ nộp tại Phòng Quản lý xuất nhập cảnh: thời hạn giải quyết không quá 08 ngày làm việc, kể từ ngày nhận đủ hồ sơ hợp lệ. 2. Đối với hồ sơ nộp tại Cục Quản lý xuất nhập cảnh: thời hạn giải quyết không quá 05 ngày làm việc, kể từ ngày nhận đủ hồ sơ hợp lệ. 3. Trường hợp có nhu cầu cần hộ chiếu gấp quy định tại Khoản 4 Điều 4 Thông tư này thì giải quyết sớm nhất trong thời hạn quy định. | 0.3687 | Có | Thời hạn giải quyết đối với hồ sơ nộp tại Phòng Quản lý xuất nhập cảnh là không quá 08 ngày làm việc kể từ ngày nhận đủ hồ sơ hợp lệ. Đối với hồ sơ nộp tại Cục Quản lý xuất nhập cảnh là không quá 05 ngày làm việc kể từ ngày nhận đủ hồ sơ hợp lệ. |
| 4 | Nếu bị mất hộ chiếu... | a) Trong thời hạn 48 giờ kể từ khi phát hiện mất hộ chiếu, cần trình báo với cơ quan Quản lý xuất nhập cảnh nơi gần nhất, theo Mẫu X08 để hủy giá trị sử dụng của hộ chiếu đã mất; b) Khi đến trình báo, cần xuất trình giấy chứng minh nhân dân hoặc thẻ Căn cước công dân còn giá trị sử dụng để kiểm tra, đối chiếu; nếu gửi đơn trình báo qua bưu điện thì đơn phải có xác nhận của Trưởng Công an phường, xã, thị trấn nơi người đó thường trú hoặc tạm trú; | 0.3961 | Có | Người dân phải trình báo trong thời hạn 48 giờ kể từ khi phát hiện mất hộ chiếu. Khi đến trình báo cần xuất trình CMND hoặc thẻ CCCD còn giá trị sử dụng. Nếu gửi đơn trình báo qua bưu điện thì đơn phải có xác nhận của Trưởng Công an phường, xã, thị trấn nơi người đó thường trú hoặc tạm trú. |
| 5 | Trong văn bản ban hành tiêu chuẩn quốc gia... | Theo đề nghị của Tổng cục trưởng Tổng cục Hậu cần - Kỹ thuật; Bộ trưởng Bộ Công an ban hành Thông tư ban hành các tiêu chuẩn quốc gia trong lĩnh vực an ninh thuộc Bộ Công an. Điều 1. Ban hành kèm theo Thông tư này 27 tiêu chuẩn quốc gia trong lĩnh vực an ninh thuộc Bộ Công an để áp dụng trong Công an nhân dân, bao gồm: STT TÊN TIÊU CHUẨN SỐ TIÊU CHUẨN 1. Thiết bị quang học nghiệp vụ Công an nhân dân - Kính lúp phân loại vân tay TCVN - AN: 020:2013 | 0.5328 | Có | Văn bản ban hành kèm theo 27 tiêu chuẩn quốc gia trong lĩnh vực an ninh thuộc Bộ Công an. Mã tiêu chuẩn của "Quy trình giám định ADN" là TCVN - AN: 035:2013. Mã tiêu chuẩn của "Quy trình giám định dữ liệu số trong các thiết bị kết nối với máy vi tính" là TCVN - AN: 041:2013. |

**Bao nhiêu queries trả về chunk relevant trong top-3?** 5 / 5

---

## 7. What I Learned (5 điểm — Demo)

**Điều hay nhất tôi học được từ thành viên khác trong nhóm:**
Tôi học được cách tổ chức metadata một cách khoa học để có thể filter dữ liệu luật một cách cực kỳ chuẩn xác theo năm ban hành hoặc theo hiệu lực (VD: metadata `status` hay `year`).

**Điều hay nhất tôi học được từ nhóm khác (qua demo):**
Qua demo, em thấy nhóm khác có ý tưởng dùng Hybrid Search (kết hợp tìm kiếm Keyword truyền thống như TF-IDF/BM25 và Vector Similarity) giúp tìm chính xác các con số và mã điều luật hơn.

**Nếu làm lại, tôi sẽ thay đổi gì trong data strategy?**
Em sẽ áp dụng kỹ thuật Parent-Child Chunking hoặc tóm tắt tài liệu bằng LLM. Thay vì embed nguyên đoạn văn bản dài, em sẽ chỉ embed bản tóm tắt hoặc tiêu đề của Điểm/Khoản đó, nhưng khi retrieve sẽ trả về toàn bộ nội dung chi tiết. Mẹo này sẽ làm tăng độ chính xác của vector lên nhiều lần.

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
