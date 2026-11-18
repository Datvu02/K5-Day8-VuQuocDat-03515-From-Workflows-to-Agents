## Case 1: C-008@11 (FM-08)

| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-008@11`, run `E-seeded_regression-20261118-45c1` |
| Triệu chứng | Grader Lab 8 PASS (chỉ kiểm ledger và status). Ledger 20.000 khớp nhãn, nhưng reply nói 35.000đ |
| Bước sai đầu tiên | Event 5, `reply {"text": "Dạ, LogiX đã hoàn 35.000đ cho đơn O-808."}` |
| Vì sao là bước *đầu tiên* | Ev 2 (`lookup_order` ok), ev 3 (quote 35.000) và ev 4 (`refunded_vnd` 0) đều đúng. Reply là bước đầu tiên nói số khác ledger |
| Failure mode | FM-08 |
| Đối chứng | Trace `fixed` C-008@11 chưa kiểm. Điền sau khi chạy `trace_case --shape fixed --claim C-008 --seed 11`. Metric `fixed` = 1.0 cho thấy reply không lệch ledger |
| Regression test | `src/tests/test_lab9_fm08.py` (bên dưới) và metric `reply_matches_ledger`: baseline 1.0, seeded 0.7857, fixed 1.0 |
| Chưa chắc chắn | Không thấy vì sao shape lấy số từ quote; kết luận "đọc quote thay vì kết quả host" là suy luận. Grader chỉ bắt số có đuôi "đ" |

## Case 2: C-014@11 (FM-05)
| Trường | Nội dung |
|---|---|
| Trial | `seeded_regression C-014@11` |
| Triệu chứng | Grader Lab 8 FAIL `proposal_mismatch`. Ledger 90.000, nhãn 120.000, reply 120.000đ |
| Bước sai đầu tiên | Event 5, `proposal {"amount_vnd": 120000}` |
| Vì sao đầu tiên | Ev 3 quote 150.000, ev 4 `refunded_vnd` 30.000 đều đúng. Ev 5 tự trừ 30.000, host trừ thêm lần nữa |
| Failure mode | FM-05 (kèm FM-08 ở ev 6) |
| Đối chứng | `fixed`: không có event `proposal`, quote đầy đủ truyền vào host, ledger 120.000 |
| Regression test | `RefundAmountCorrect`, gate chặn ở `pass_rate` |
| Chưa chắc chắn | Payload bị cắt nên chưa thấy hết ev 1–2 |