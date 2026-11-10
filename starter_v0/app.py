from __future__ import annotations

import uuid
from datetime import datetime
from pathlib import Path

import streamlit as st

from chat import now_iso, run_model_tool_loop, trim_history, write_transcript
from env_loader import load_lab_env
from providers import make_provider
from tools import load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version


ROOT = Path(__file__).parent
ARTIFACTS = ROOT / "artifacts"
PROMPT_PATH = ARTIFACTS / "system_prompt.md"
TOOLS_PATH = ARTIFACTS / "tools.yaml"
VERSION = "tools-v1"
load_lab_env(ROOT)


@st.cache_resource
def get_provider():
    return make_provider("openrouter")


def get_runtime():
    declarations = load_tool_declarations(TOOLS_PATH)
    return get_provider(), to_openai_tools(declarations), PROMPT_PATH.read_text(encoding="utf-8")


st.set_page_config(page_title="Research Agent", page_icon="🔎", layout="centered")
st.title("🔎 Research Agent")
st.caption("Tìm bài đăng, tra cứu web/tin tức, đọc URL và tổng hợp digest.")

with st.sidebar:
    st.subheader("Công cụ")
    st.markdown(
        "- Timeline theo tài khoản hoặc khoảng ngày\n"
        "- Tìm bài đăng theo chủ đề\n"
        "- Tra cứu web và tin tức\n"
        "- Đọc URL và định dạng digest\n"
        "- Xác định tài khoản, gộp tin trùng, đối chiếu phát biểu\n"
        "- Gửi Telegram sau khi xác nhận"
    )
    st.caption(f"Model: OpenRouter · Artifact: {VERSION}")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "transcript" not in st.session_state:
    artifact = build_artifact_version(VERSION, PROMPT_PATH, TOOLS_PATH)
    transcript_id = f"{VERSION}_openrouter_{datetime.now().strftime('%Y%m%dT%H%M%S%f')}_{uuid.uuid4().hex[:6]}"
    st.session_state.transcript = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact),
        "provider": "openrouter",
        "model": "openai/gpt-4o-mini",
        "system_prompt": str(PROMPT_PATH),
        "tools": str(TOOLS_PATH),
        "history_window": 5,
        "max_tool_rounds": 6,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if user_text := st.chat_input("Hỏi về tin tức, bài đăng hoặc một URL..."):
    st.session_state.chat_history.append({"role": "user", "content": user_text})
    with st.chat_message("user"):
        st.markdown(user_text)

    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý..."):
            try:
                provider, tool_specs, system_prompt = get_runtime()
                turn_artifact = artifact_version_dict(build_artifact_version(VERSION, PROMPT_PATH, TOOLS_PATH))
                messages = [
                    {"role": "system", "content": system_prompt},
                    *trim_history(st.session_state.chat_history[:-1], 5),
                    {"role": "user", "content": user_text},
                ]
                result = run_model_tool_loop(
                    provider=provider,
                    messages=messages,
                    tools=tool_specs,
                    model=None,
                    max_tool_rounds=6,
                )
                answer = result["assistant_text"] or "Đã hoàn tất."
                st.markdown(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.session_state.transcript["turns"].append({
                    "turn_index": len(st.session_state.transcript["turns"]) + 1,
                    "started_at": now_iso(),
                    "ended_at": now_iso(),
                    "user": user_text,
                    **turn_artifact,
                    **result,
                })
            except Exception as exc:
                answer = f"Lỗi khi gọi agent: {type(exc).__name__}: {exc}"
                st.error(answer)
                st.session_state.chat_history.append({"role": "assistant", "content": answer})
                st.session_state.transcript["turns"].append({
                    "turn_index": len(st.session_state.transcript["turns"]) + 1,
                    "started_at": now_iso(),
                    "ended_at": now_iso(),
                    "user": user_text,
                    "status": "provider_error",
                    "error": f"{type(exc).__name__}: {exc}",
                })

    transcript_path = ROOT / "transcripts" / f"{st.session_state.transcript['transcript_id']}.transcript.json"
    write_transcript(transcript_path, st.session_state.transcript)
    st.rerun()
