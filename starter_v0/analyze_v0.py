
import pandas as pd

# Đổi thành đường dẫn CSV kết quả thực tế của bạn
df = pd.read_csv(r"D:\Linh\day4\K5-L3A-DAY03-TEAM4CHANGLINHNGULAM-Prompt-Function-Calling-Tool-Design-MCP\starter_v0\analysis\base_runs.csv")

# Chỉ lấy run hợp lệ
run_id = "v0_B_base_openrouter_20261110T104223427707"

v0 = df[df["run_id"] == run_id].copy()

# Chuyển passed về boolean an toàn
v0["passed"] = (
    v0["passed"].astype(str).str.lower() == "true"
)

# Lọc các case FAIL
failed = v0[~v0["passed"]].copy()

# Phân loại theo lỗi quan sát thực tế
failure_types = {
    "R03_web_news_routing": "wrong_arg_value",
    "R08_out_of_scope": "out_of_scope",
    "R10_missing_handle": "missing_info",
    "R11_missing_url": "missing_info",
    "R12_confirm_before_send": "wrong_boundary",
    "R13_parallel_web_and_tweets": "wrong_arg_value",
    "R14_out_of_scope_coding": "out_of_scope",
}

failed["actual_failure_type"] = (
    failed["case_id"].map(failure_types)
)

columns = [
    "case_id",
    "actual_failure_type",
    "observed_mismatch",
    "expected_tool",
    "actual_tool",
    "failures",
]

print(f"Total: {len(v0)}")
print(f"PASS: {v0['passed'].sum()}")
print(f"FAIL: {len(failed)}")

print(failed[columns].to_string(index=False))

failed[columns].to_csv(
    "v0_failure_analysis.csv",
    index=False,
    encoding="utf-8-sig"
)
