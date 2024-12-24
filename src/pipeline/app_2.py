from src.agents.react import run as run_react_agent
from src.config.setup import GOOGLE_ICON_PATH
from src.config.setup import PROJECT_ROOT
from src.config.logging import logger
import streamlit as st
import importlib.util
import json
import ast
import re
import os


def load_available_apps():
    """
    (No longer used in the UI, but kept for reference.)
    Searches for generated apps in ./src/apps/ and populates session state
    with a dictionary of {app_name: path_to_frontend_py}.
    """
    apps_base_dir = os.path.join(PROJECT_ROOT, 'src', 'apps')
    if "available_apps" not in st.session_state:
        st.session_state["available_apps"] = {}
    st.session_state["available_apps"].clear()

    if os.path.exists(apps_base_dir):
        for entry in os.listdir(apps_base_dir):
            d_path = os.path.join(apps_base_dir, entry)
            if os.path.isdir(d_path):
                frontend_path = os.path.join(d_path, "frontend.py")
                if os.path.exists(frontend_path):
                    st.session_state["available_apps"][entry] = os.path.relpath(frontend_path, start='.')


def run_app(app_path: str) -> None:
    """
    Dynamically imports and executes the main() function from a generated app.
    (No longer used in the UI, but kept for reference.)
    """
    try:
        spec = importlib.util.spec_from_file_location("generated_app", app_path)
        generated_app = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(generated_app)

        if hasattr(generated_app, 'main'):
            generated_app.main()
        else:
            raise AttributeError("The selected app does not have a main() function to run.")
    except Exception as e:
        app_name_slug = os.path.basename(os.path.dirname(app_path))
        st.session_state["run_error"] = {
            "app_name_slug": app_name_slug,
            "error_message": str(e)
        }
        return


# ==================================================================
#  QnA Agent Experience & Trace Rendering
# ==================================================================

def linkify_urls(text: str) -> str:
    """
    Finds URLs in a string and makes them clickable HTML links.
    """
    url_pattern = re.compile(r"(http[s]?://\S+)")
    return url_pattern.sub(r"<a href='\g<0>' target='_blank' style='color: #1f77b4;'>\g<0></a>", text)


def dict_to_html(data) -> str:
    """
    Recursively convert a Python dict (or list) into an HTML bullet list.
    """
    if isinstance(data, dict):
        items_html = ""
        for k, v in data.items():
            items_html += f"<li><strong>{k}</strong>: {dict_to_html(v)}</li>"
        return f"<ul style='margin:0 0 0 20px; padding:0;'>{items_html}</ul>"
    elif isinstance(data, list):
        items_html = ""
        for elem in data:
            items_html += f"<li>{dict_to_html(elem)}</li>"
        return f"<ul style='margin:0 0 0 20px; padding:0;'>{items_html}</ul>"
    else:
        # It's a scalar, linkify if it's a string
        text_str = str(data)
        text_str = linkify_urls(text_str)
        return text_str


def parse_and_format_json_or_dict(content: str) -> str:
    """
    1) Try to parse `content` as a *Python dict* using `ast.literal_eval`.
    2) If that fails, try to parse as JSON.
    3) Otherwise, just linkify the text as-is.
    """
    # Attempt Python dict parse
    try:
        if (content.strip().startswith("{") and content.strip().endswith("}")) or \
           (content.strip().startswith("[") and content.strip().endswith("]")):
            data = ast.literal_eval(content)
            html = dict_to_html(data)
            return html
    except Exception:
        pass

    # Attempt JSON parse
    try:
        data = json.loads(content)
        html = dict_to_html(data)
        return html
    except Exception:
        pass

    # Just linkify the raw text
    return linkify_urls(content)


def parse_agent_trace() -> None:
    """
    Reads the agent's trace file (./data/trace.txt), parses it into iterations,
    and renders each iteration in its own collapsible section with smaller font,
    skipping Observations, etc.
    """
    trace_file = "./data/trace.txt"
    if not os.path.exists(trace_file):
        st.warning("No trace file found. Please ask a question first.")
        return

    iteration_data = {}
    current_iteration = 0
    iteration_data[current_iteration] = {
        "thoughts": [],
        "actions": [],
        "errors": [],
        "answer": None,
        "tools_used": []
    }

    def ensure_iteration(i):
        if i not in iteration_data:
            iteration_data[i] = {
                "thoughts": [],
                "actions": [],
                "errors": [],
                "answer": None,
                "tools_used": []
            }

    with open(trace_file, "r", encoding="utf-8") as f:
        for line in f:
            line = line.rstrip("\n")

            # Detect iteration lines like: "Iteration 0" or "Iteration 1"
            if line.startswith("Iteration "):
                parts = line.split()
                if len(parts) == 2 and parts[0] == "Iteration":
                    current_iteration = int(parts[1])
                    ensure_iteration(current_iteration)
                continue

            # Hide Observations => skip lines with "system: Observation"
            if "system: Observation" in line:
                continue

            # assistant: Thought:
            if "assistant: Thought:" in line:
                content = line.split("assistant: Thought:")[-1].strip()
                iteration_data[current_iteration]["thoughts"].append(content)
                continue

            # assistant: Action:
            if "assistant: Action:" in line:
                content = line.split("assistant: Action:")[-1].strip()
                iteration_data[current_iteration]["actions"].append(content)
                if "Using Name." in content:
                    # If line is "assistant: Action: Using Name.FOO tool"
                    tool_str = content.split("Using Name.")[1].split(" tool")[0]
                    iteration_data[current_iteration]["tools_used"].append(tool_str)
                continue

            # assistant: Final Answer:
            if "assistant: Final Answer:" in line:
                content = line.split("assistant: Final Answer:")[-1].strip()
                iteration_data[current_iteration]["answer"] = content
                continue

            # If there's an error mention
            if "Error:" in line or "Unhandled exception" in line:
                iteration_data[current_iteration]["errors"].append(line)
                continue

    # Lighter pastel colors for iteration sections
    pastel_colors = [
        "#FFE6EC",  # lighter pink
        "#E6FFE9",  # lighter green
        "#E6EEFF",  # lighter blue
        "#FFF6E6",  # lighter peach
        "#FAE6FF",  # lighter purple
    ]

    all_tools_used_in_order = []
    iteration_indices = sorted(iteration_data.keys())

    # Render each iteration's data
    for i in iteration_indices:
        data = iteration_data[i]
        # Skip if there's no relevant content
        if not (data["thoughts"] or data["actions"] or data["errors"] or data["answer"]):
            continue

        with st.expander(f"Iteration {i}", expanded=(i == 0)):
            color = pastel_colors[i % len(pastel_colors)]

            # THOUGHTS
            for t in data["thoughts"]:
                t_html = parse_and_format_json_or_dict(t)
                st.markdown(f"""
                <div style="background-color:{color}; padding:8px; margin:4px 0; border-radius:5px; font-size:13px;">
                    <strong>Thought:</strong> {t_html}
                </div>
                """, unsafe_allow_html=True)

            # ACTIONS
            for a in data["actions"]:
                a_html = parse_and_format_json_or_dict(a)
                st.markdown(f"""
                <div style="background-color:{color}; padding:8px; margin:4px 0; border-radius:5px; font-size:13px; border-left:3px solid #666;">
                    <strong>Action:</strong> {a_html}
                </div>
                """, unsafe_allow_html=True)

            # ERRORS
            for err in data["errors"]:
                err_html = parse_and_format_json_or_dict(err)
                st.markdown(f"""
                <div style="background-color:#FFCCCC; padding:8px; margin:4px 0; border-radius:5px; border:2px solid #AA0000; font-size:13px;">
                    <strong style="color:#AA0000;">Error:</strong> {err_html}
                </div>
                """, unsafe_allow_html=True)

            # Final Answer
            if data["answer"]:
                ans_html = parse_and_format_json_or_dict(data["answer"])
                st.markdown(f"""
                <div style="background-color:{color}; padding:10px; margin:10px 0; border-radius:8px; font-size:14px;">
                    <strong>Final Answer:</strong> {ans_html}
                </div>
                """, unsafe_allow_html=True)

            # Collect tools in order
            all_tools_used_in_order.extend(data["tools_used"])

    # If any tools used, display in final summary
    if all_tools_used_in_order:
        st.markdown("<hr>", unsafe_allow_html=True)
        st.markdown("<h4>APIs (Tools) Used in Order</h4>", unsafe_allow_html=True)
        for idx, tool in enumerate(all_tools_used_in_order, start=1):
            st.markdown(f"- **Step {idx}:** `{tool}`")


def display_qna_experience():
    """
    Displays the final answer (if any), then the trace expansions.
    """
    st.subheader("QnA Trace")
    final_answer = st.session_state.get("agent_final_answer", None)
    if final_answer:
        # parse final answer for python dict or JSON or raw
        answer_html = parse_and_format_json_or_dict(final_answer)
        st.markdown(f"""
        <div style="border: 2px solid #ccc; border-radius:8px; padding:20px; background-color:#fafafa;">
            <h3 style="margin-top:0;">Final Answer</h3>
            <div style="font-size:13px;">
                {answer_html}
            </div>
        </div>
        """, unsafe_allow_html=True)

    parse_agent_trace()


def run():
    st.set_page_config(
        page_title="Agentic App Builder",
        layout="wide",
        page_icon="💡",
        initial_sidebar_state="expanded"
    )

    # Path to the trace file
    trace_file_path = "./data/trace.txt"

    # Add some CSS for a more colorful, eye-catching title
    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&display=swap');
        body {
            font-family: 'Nunito Sans', 'Helvetica', sans-serif;
            font-size: 14px;
            color: #333;
            background-color: #f8f8f8;
        }
        h1, h2, h3, h4 {
            font-family: 'Cascadia Code', 'Monaco', monospace;
            color: #222;
        }
        .google-search-box {
            max-width: 600px;
            margin: auto;
        }
        .google-search-input {
            width: 100%;
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #ccc;
            border-radius: 24px;
            outline: none;
            transition: border-color 0.2s;
        }
        .google-search-input:focus {
            border-color: #4285f4;
        }
        .search-button {
            margin-top: 10px;
            font-size: 16px;
            padding: 10px 20px;
            border-radius: 24px;
        }
        /* Updated rainbow style for the main title */
        .rainbow-text {
            background: linear-gradient(
              to right, 
              red, 
              orange, 
              yellow, 
              green, 
              blue, 
              indigo, 
              violet
            );
            -webkit-background-clip: text;
            color: transparent;
            font-size: 3rem;
            font-weight: 700;
            margin-bottom: 20px;
            text-align: center;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # Initialize session state for final answer if not present
    if "agent_final_answer" not in st.session_state:
        st.session_state["agent_final_answer"] = ""

    # ====================
    # Sidebar
    # ====================
    with st.sidebar:
        if os.path.exists(GOOGLE_ICON_PATH):
            st.image(GOOGLE_ICON_PATH, width=40)

        # Button to clear traces at any time
        if st.button("Clear Traces"):
            if os.path.exists(trace_file_path):
                os.remove(trace_file_path)
            st.success("Traces have been cleared.")
            # Refresh the app so user sees that traces are gone
            st.rerun()

        # Number input for max iterations
        max_iterations = st.number_input(
            "Max Iterations",
            min_value=1,
            max_value=20,
            value=3,  # default
            step=1,
            help="Set how many reasoning steps the agent can perform."
        )

        # If previously an error occurred running some app
        if "run_error" in st.session_state:
            app_name_slug = st.session_state["run_error"]["app_name_slug"]
            error_message = st.session_state["run_error"]["error_message"]
            st.error(f"Error running the app: {error_message}")

    # ====================
    # Main Body
    # ====================

    # Eye-catching Title
    st.markdown("<h1 class='rainbow-text'>Agentic Search</h1>", unsafe_allow_html=True)

    # "Google-like" Search Box
    st.write("<div class='google-search-box'>", unsafe_allow_html=True)
    user_query = st.text_input(
        "",
        key="explore_question",
        label_visibility="collapsed",
        placeholder="Ask anything...",
        help="Type your question here!",
    )
    st.write("</div>", unsafe_allow_html=True)

    search_clicked = st.button(
        "Search",
        key="search_button",
        type="primary",
        help="Ask the Gemini React Agent",
        use_container_width=False
    )

    if search_clicked and user_query.strip():
        # 1) Clear old final answer
        st.session_state["agent_final_answer"] = ""

        # 2) Clear the old trace file so each new query is fresh
        if os.path.exists(trace_file_path):
            os.remove(trace_file_path)

        # 3) Run the agent
        query = st.session_state["explore_question"]
        final_answer = run_react_agent(query, max_iterations)
        st.session_state["agent_final_answer"] = final_answer

        # 4) Rerun the app so that parse_agent_trace() can pick up new contents
        st.rerun()

    # Show QnA Experience and Trace
    display_qna_experience()


if __name__ == "__main__":
    try:
        run()
    except Exception as e:
        logger.error("Unhandled exception in main: %s", e)
        st.error(f"An unexpected error occurred: {e}")
