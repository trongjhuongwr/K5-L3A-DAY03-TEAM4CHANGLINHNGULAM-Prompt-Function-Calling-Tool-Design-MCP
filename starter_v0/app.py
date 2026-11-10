from __future__ import annotations

import json
import sys
from datetime import datetime
from pathlib import Path
from typing import Any

import streamlit as st

# Setup paths and environment
ROOT = Path(__file__).resolve().parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from env_loader import load_lab_env
load_lab_env(ROOT)

from chat import (
    now_iso,
    run_model_tool_loop,
    safe_slug,
    write_transcript,
)
from providers import make_provider
from tools import TOOL_FUNCTIONS, load_tool_declarations, to_openai_tools
from versioning import artifact_version_dict, build_artifact_version

ARTIFACTS_DIR = ROOT / "artifacts"
TRANSCRIPTS_DIR = ROOT / "transcripts"
TRANSCRIPTS_DIR.mkdir(parents=True, exist_ok=True)

st.set_page_config(
    page_title="Research Agent — Day 03 Lab",
    page_icon="🤖",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stChatMessage {
        padding: 0.8rem 1rem;
        border-radius: 0.6rem;
    }
    .tool-box {
        background-color: #f0f2f6;
        border-left: 4px solid #4f46e5;
        padding: 8px 12px;
        margin: 6px 0;
        border-radius: 4px;
        font-size: 0.9rem;
    }
    .stBadge {
        background-color: #e0e7ff;
        color: #3730a3;
        padding: 2px 8px;
        border-radius: 12px;
        font-size: 0.8rem;
        font-weight: 600;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "working_history" not in st.session_state:
    # Used for maintaining LLM multi-turn context
    st.session_state.working_history = []

if "transcript" not in st.session_state:
    st.session_state.transcript = None

if "transcript_path" not in st.session_state:
    st.session_state.transcript_path = None


def init_transcript(provider_name: str, model_name: str, version_label: str, system_path: Path, tools_path: Path):
    timestamp = datetime.now().strftime("%Y%m%dT%H%M%S%f")
    transcript_id = "_".join([
        safe_slug(version_label),
        safe_slug(provider_name),
        timestamp,
    ])
    artifact_version = build_artifact_version(version_label, system_path, tools_path)
    path = TRANSCRIPTS_DIR / f"{transcript_id}.transcript.json"

    transcript_data = {
        "transcript_id": transcript_id,
        **artifact_version_dict(artifact_version),
        "provider": provider_name,
        "model": model_name,
        "system_prompt": str(system_path),
        "tools": str(tools_path),
        "history_window": 5,
        "max_tool_rounds": 4,
        "created_at": now_iso(),
        "updated_at": now_iso(),
        "turns": [],
    }
    st.session_state.transcript = transcript_data
    st.session_state.transcript_path = path
    write_transcript(path, transcript_data)


# ---------------- SIDEBAR ----------------
with st.sidebar:
    st.title("🤖 Research Agent")
    st.caption("AI20k Lab Day 03 • Evidence-driven Agent")
    st.divider()

    st.subheader("⚙️ Cấu hình Model & Version")
    provider_option = st.selectbox(
        "Provider",
        options=["openrouter", "openai", "gemini", "anthropic", "ollama"],
        index=0,
    )
    
    version_label = st.text_input("Artifact Version", value="v0", help="Ví dụ: v0, v1, v2, v3")
    max_rounds = st.slider("Max Tool Rounds", min_value=1, max_value=6, value=4)

    system_prompt_file = ARTIFACTS_DIR / "system_prompt.md"
    tools_file = ARTIFACTS_DIR / "tools.yaml"

    try:
        tool_declarations = load_tool_declarations(tools_file)
        openai_tools = to_openai_tools(tool_declarations)
        provider = make_provider(provider_option)
        selected_model = getattr(provider, "default_model", "default")
        current_artifact = build_artifact_version(version_label, system_prompt_file, tools_file)
        st.success(f"**Version:** `{current_artifact.artifact_version}`")
    except Exception as e:
        st.error(f"Lỗi nạp config/provider: {e}")
        st.stop()

    if st.session_state.transcript is None:
        init_transcript(provider_option, selected_model, version_label, system_prompt_file, tools_file)

    st.divider()

    # Session Management
    col_reset, col_down = st.columns(2)
    with col_reset:
        if st.button("🔄 Tạo phiên mới", use_container_width=True):
            st.session_state.messages = []
            st.session_state.working_history = []
            init_transcript(provider_option, selected_model, version_label, system_prompt_file, tools_file)
            st.rerun()

    with col_down:
        if st.session_state.transcript_path and st.session_state.transcript_path.exists():
            transcript_content = st.session_state.transcript_path.read_text(encoding="utf-8")
            st.download_button(
                label="📥 Tải Transcript",
                data=transcript_content,
                file_name=st.session_state.transcript_path.name,
                mime="application/json",
                use_container_width=True,
            )

    st.divider()

    # Tool Explorer
    with st.expander(f"🛠️ Danh sách Tool ({len(tool_declarations)} tools)", expanded=False):
        for t in tool_declarations:
            st.markdown(f"**`{t['name']}`**: {t.get('description', '')}")
            req = t.get('parameters', {}).get('required', [])
            if req:
                st.caption(f"Required args: `{', '.join(req)}`")
            st.markdown("---")

    # Sample queries
    with st.expander("💡 Câu hỏi mẫu để thử nhanh", expanded=True):
        samples = [
            "Tin tức AI hôm nay có gì nổi bật?",
            "Tweet mới nhất của Sam Altman là gì?",
            "Mọi người đang bàn gì về GPT-5 trên Twitter?",
            "Tóm tắt bài này: https://openai.com/research/",
            "Tìm bài báo mới nhất về Agent Evaluation trên arXiv",
            "Đăng bản tin này lên Telegram giúp mình",
        ]
        for s in samples:
            if st.button(s, key=f"sample_{s}", use_container_width=True):
                st.session_state.preset_prompt = s
                st.rerun()


# ---------------- MAIN CHAT AREA ----------------
st.title("🔬 Research Agent Interactive Playground")
st.markdown("Agent có khả năng tìm kiếm web (`lookup`), mạng xã hội (`timeline`, `social_search`), đọc URL (`fetch`), tra cứu tài liệu (`papers`, `policy`), và tương tác hỏi lại người dùng (`clarify`).")

# Render message history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])
        if "tool_events" in msg and msg["tool_events"]:
            with st.expander(f"🔍 Xem {len(msg['tool_events'])} lượt gọi công cụ (Tool Calls)", expanded=False):
                for event in msg["tool_events"]:
                    t_name = event.get("tool")
                    t_args = event.get("args")
                    t_res = event.get("result")
                    st.markdown(f"**Tool:** `{t_name}`")
                    st.json({"arguments": t_args, "result": t_res})
                    st.divider()

# Handle Preset Prompt if clicked from sidebar
preset = st.session_state.pop("preset_prompt", None)
user_input = st.chat_input("Nhập câu hỏi hoặc yêu cầu cho Research Agent...") or preset

if user_input:
    # 1. Add and display user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # 2. Build messages for LLM
    system_text = system_prompt_file.read_text(encoding="utf-8")
    
    # Keep rolling history (history_window = 5 pairs)
    trimmed_context = st.session_state.working_history[-10:]
    llm_messages = [{"role": "system", "content": system_text}] + trimmed_context + [{"role": "user", "content": user_input}]

    # 3. Run Agent Loop
    with st.chat_message("assistant"):
        with st.spinner("Đang xử lý và gọi công cụ..."):
            try:
                loop_result = run_model_tool_loop(
                    provider=provider,
                    messages=llm_messages,
                    tools=openai_tools,
                    model=selected_model,
                    max_tool_rounds=max_rounds,
                )
            except Exception as e:
                st.error(f"Lỗi khi thực thi Agent: {e}")
                st.stop()

        assistant_text = loop_result.get("assistant_text", "")
        tool_events = loop_result.get("tool_events", [])
        status = loop_result.get("status")

        # Display Assistant response
        st.markdown(assistant_text)

        # Display tool call details if any tools were executed
        if tool_events:
            with st.expander(f"🔍 Xem {len(tool_events)} lượt gọi công cụ (Tool Calls)", expanded=True):
                for event in tool_events:
                    t_name = event.get("tool")
                    t_args = event.get("args")
                    t_res = event.get("result")
                    st.markdown(f"**Tool:** `{t_name}`")
                    st.json({"arguments": t_args, "result": t_res})
                    st.divider()

        if status == "waiting_for_user":
            st.info("ℹ️ **Agent đang đợi phản hồi thêm hoặc xác nhận từ bạn.** Vui lòng trả lời câu hỏi trên.")

        # Update Session State Messages
        st.session_state.messages.append({
            "role": "assistant",
            "content": assistant_text,
            "tool_events": tool_events,
            "status": status,
        })

        # Update working history for multi-turn
        st.session_state.working_history.append({"role": "user", "content": user_input})
        st.session_state.working_history.append({"role": "assistant", "content": assistant_text})

        # Update Transcript on disk
        if st.session_state.transcript and st.session_state.transcript_path:
            turn_record = {
                "turn": len(st.session_state.transcript["turns"]) + 1,
                "timestamp": now_iso(),
                "user_text": user_input,
                "status": status,
                "assistant_text": assistant_text,
                "rounds": loop_result.get("rounds", []),
            }
            st.session_state.transcript["turns"].append(turn_record)
            write_transcript(st.session_state.transcript_path, st.session_state.transcript)
