# Judge audit

Chạy: `python -m lab9.judge --csv <file> --audit 5`

| Tiêu chí | n | κ | Precision | Recall | Đạt FLOORS (κ≥0.6, P≥0.8, R≥0.7)? | Quyết định |
|---|---|---|---|---|---|---|
| tone_ok | 100 | 0.757 | 0.857 | 0.80 | Đạt cả ba | dùng |
| helpful | 100 | 0.375 | 1.0 | 0.30 | Không (κ và R dưới sàn) | loại |

Ma trận nhầm lẫn (FAIL là lớp dương): tone_ok tp 24 / fp 4 / fn 6 / tn 66; helpful tp 9 / fp 0 / fn 21 / tn 70.
Tỉ lệ fail quan sát → hiệu chỉnh Rogan-Gladen: tone_ok 0.28 → 0.30; helpful 0.09 → 0.30.

## ≥5 case audit thủ công
| # | Case | Judge nói | Người nói | Ai đúng? | Ghi chú |
|---|---|---|---|---|---|
| 1 | H-008 "Em đã hoàn tiền cho anh rồi nha…" (tone) | PASS | FAIL | Người (theo nhãn) | Xưng hô thân mật, giả thuyết: judge bỏ sót lỗi giọng điệu |
| 2 | H-017 "Dạ, bạn ơi LogiX đã hoàn 25.000đ…" (tone) | PASS | FAIL | Người (theo nhãn) | "bạn ơi… nha" quá suồng sã |
| 3 | H-029 "Dạ, vui lòng chờ… không cần nhắn thêm." (tone) | PASS | FAIL | Người (theo nhãn) | Câu cộc, gạt khách |
| 4 | H-042 "…Tiền về trong 3–5 ngày ạ." (tone) | FAIL | PASS | Cần bạn đọc lại | Giả thuyết: judge nhạy với lời hứa thời gian |
| 5 | H-051 "…đã refund 90.000đ…" (tone) | FAIL | PASS | Cần bạn đọc lại | Giả thuyết: judge bị từ vay mượn "refund" |
| 6 | HL-015, HL-020 "đã hoàn X đồng cho đơn Y ạ" (helpful) | PASS | FAIL | Người (theo nhãn) | Chỉ nêu số tiền, thiếu thông tin tiếp theo |
| 7 | HL-016, HL-028, HL-035 (helpful) | PASS | FAIL | Người (theo nhãn) | Toàn lời xin lỗi, không có hành động; judge bị lời lẽ lịch sự đánh lừa |

## Kết luận
- Loại judge helpful: recall 0.30 (bỏ sót 21/30 ca fail thật), κ 0.375. Dùng nó trong gate sẽ báo "ổn" trong khi khoảng 30% câu trả lời không hữu ích.
- tone_ok dùng được nhưng recall chỉ hơn sàn 0.7 một khoảng nhỏ.
- Tiền và approval luôn chấm bằng code, không dùng judge.
- Rủi ro còn lại: judge chỉ được kiểm trên dữ liệu replay đã công khai; cần nhãn người mới để có held-out thật.