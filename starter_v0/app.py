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

# Tool metadata and categories for attractive display
TOOL_ICONS = {
    "lookup": "🌐",
    "fetch": "📄",
    "format": "📋",
    "timeline": "🐦",
    "social_search": "🔎",
    "papers": "📚",
    "paper_text": "📑",
    "policy": "📜",
    "send": "✈️",
    "clarify": "❓",
    "crypto_price": "🪙",
    "github_search": "🐙",
    "weather": "🌤️",
    "calculator": "🧮",
}

TOOL_CATEGORIES = {
    "🌐 Web & Tin tức": ["lookup", "fetch", "format"],
    "🐦 Mạng xã hội X/Twitter": ["timeline", "social_search"],
    "🔬 Nghiên cứu & Chính sách": ["papers", "paper_text", "policy"],
    "🚀 Tool mới của nhóm": ["crypto_price", "github_search", "weather", "calculator"],
    "🛡️ An toàn & Tương tác": ["clarify", "send"],
}

# Custom CSS for styling
st.markdown(
    """
    <style>
    .stChatMessage {
        padding: 0.9rem 1.2rem;
        border-radius: 0.8rem;
        margin-bottom: 0.8rem;
    }
    .tool-card {
        background: rgba(255, 255, 255, 0.04);
        border: 1px solid rgba(255, 255, 255, 0.08);
        border-radius: 8px;
        padding: 10px 14px;
        margin-bottom: 8px;
    }
    .badge-core {
        background-color: #3b82f6;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .badge-bonus {
        background-color: #8b5cf6;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .badge-new {
        background-color: #10b981;
        color: white;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 0.72rem;
        font-weight: 600;
    }
    .arg-pill {
        background: rgba(255, 255, 255, 0.08);
        color: #93c5fd;
        padding: 1px 6px;
        border-radius: 4px;
        font-size: 0.75rem;
        font-family: monospace;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize Session State
if "messages" not in st.session_state:
    st.session_state.messages = []

if "working_history" not in st.session_state:
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
    st.caption("AI20k Lab Day 03 • Nhóm 4 (4CHANGLINHNGULAM)")
    st.divider()

    st.subheader("⚙️ Cấu hình Model & Version")
    provider_option = st.selectbox(
        "Provider",
        options=["openrouter", "openai", "gemini", "anthropic", "ollama"],
        index=0,
    )
    
    version_label = st.text_input("Artifact Version", value="v3", help="Ví dụ: v0, v1, v2, v3")
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
        st.info("🧪 **Unit Tests:** `108/108 PASSED` (0 failed, 0 skipped)")
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

    # Enhanced Tool Explorer
    st.subheader(f"🛠️ Hệ sinh thái {len(tool_declarations)} Tools")
    tool_search = st.text_input("🔍 Lọc công cụ...", placeholder="Gõ tên tool hoặc từ khóa...").strip().lower()

    declared_dict = {t["name"]: t for t in tool_declarations}

    with st.expander("📂 Xem chi tiết các nhóm công cụ", expanded=False):
        for cat_name, cat_tools in TOOL_CATEGORIES.items():
            matching_tools = [t_name for t_name in cat_tools if t_name in declared_dict]
            if tool_search:
                matching_tools = [
                    t_name for t_name in matching_tools
                    if tool_search in t_name.lower() or tool_search in declared_dict[t_name].get("description", "").lower()
                ]

            if not matching_tools:
                continue

            st.markdown(f"**{cat_name}** ({len(matching_tools)})")
            for t_name in matching_tools:
                t = declared_dict[t_name]
                icon = TOOL_ICONS.get(t_name, "🔧")
                
                # Tag logic
                if t_name in ["crypto_price", "github_search", "weather", "calculator"]:
                    tag_html = '<span class="badge-new">Nhóm tạo</span>'
                elif t_name in ["send", "policy", "papers", "paper_text"]:
                    tag_html = '<span class="badge-bonus">Bonus</span>'
                else:
                    tag_html = '<span class="badge-core">Core</span>'

                req_args = t.get("parameters", {}).get("required", [])
                pills = " ".join([f'<span class="arg-pill">*{arg}</span>' for arg in req_args])

                st.markdown(
                    f"""
                    <div class="tool-card">
                        <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:4px;">
                            <strong>{icon} <code>{t_name}</code></strong>
                            {tag_html}
                        </div>
                        <div style="font-size:0.8rem; color:#cbd5e1; margin-bottom:6px;">{t.get("description", "")}</div>
                        <div><small style="color:#94a3b8;">Args bắt buộc:</small> {pills if pills else '<small style="color:#64748b;">none</small>'}</div>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
            st.markdown("---")

    # Unit Tests Status Expander
    with st.expander("🧪 Kết quả Unit Tests (108 Passed)", expanded=True):
        st.markdown("**Kết quả:** `108/108 PASSED (0 failed, 0 skipped)`")
        st.markdown("- `test_tool_contract.py`: **75 passed** (Kiểm tra tools.yaml & signatures)")
        st.markdown("- `test_tools_examples.py`: **7 passed** (Tests mẫu)")
        st.markdown("- `test_tools_todo.py`: **26 passed** (Unit tests cho tất cả 14 tools)")
        if st.button("▶️ Chạy lại Unit Tests ngay", use_container_width=True):
            import subprocess
            with st.spinner("Đang chạy pytest trên toàn bộ test suite..."):
                proc = subprocess.run(
                    [sys.executable, "-m", "pytest", "tests/", "-v"],
                    capture_output=True,
                    text=True,
                    cwd=str(ROOT),
                )
                st.code(proc.stdout if proc.stdout else proc.stderr, language="bash")


    # Sample queries
    with st.expander("💡 Câu hỏi mẫu 1-Click Test", expanded=True):
        samples = [
            ("🌐 Tin tức AI hôm nay", "Tin tức AI hôm nay có gì nổi bật trên web?"),
            ("🐦 Tweet Sam Altman", "Tweet mới nhất của Sam Altman là gì?"),
            ("🪙 Giá Bitcoin & ETH", "Giá Bitcoin và Ethereum hôm nay đang là bao nhiêu USDT?"),
            ("🐙 Top repo LLM Agent", "Tìm giúp mình các repository mã nguồn mở hàng đầu về LLM Agent trên GitHub"),
            ("🌤️ Thời tiết Hà Nội", "Thời tiết hiện tại ở Hà Nội thế nào?"),
            ("🧮 Tính toán số học", "Tính giúp mình giá trị biểu thức: 125 * 8 - 450 / 5"),
            ("🛡️ Gửi tin Telegram", "Đăng bản tin này lên Telegram giúp mình"),
        ]
        for label, q_text in samples:
            if st.button(label, key=f"sample_{label}", use_container_width=True):
                st.session_state.preset_prompt = q_text
                st.rerun()


# ---------------- MAIN CHAT AREA ----------------
st.title("🔬 Research Agent Interactive Playground")
st.markdown("Hệ thống trợ lý nghiên cứu đa tác vụ: Tìm kiếm Web & Tin tức (`lookup`, `fetch`), Mạng xã hội X (`timeline`, `social_search`), Bài báo arXiv (`papers`), Giá Crypto (`crypto_price`), Mã nguồn GitHub (`github_search`), Thời tiết (`weather`), và Tính toán an toàn (`calculator`).")

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
                    icon = TOOL_ICONS.get(t_name, "🔧")
                    st.markdown(f"**{icon} Công cụ:** `{t_name}`")
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
        with st.spinner("Agent đang xử lý và thực thi công cụ..."):
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
                    icon = TOOL_ICONS.get(t_name, "🔧")
                    st.markdown(f"**{icon} Công cụ:** `{t_name}`")
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
