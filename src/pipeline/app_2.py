import streamlit as st
import json
import re
import ast
import os
import time

from src.agents.react import run_react_agent
from src.config.setup import GOOGLE_ICON_PATH
from src.config.logging import logger

# Utility Functions remain the same
def linkify_urls(text: str) -> str:
    url_pattern = re.compile(r"(http[s]?://\S+)")
    return url_pattern.sub(
        r"<a href='\g<0>' target='_blank' style='color: #1f77b4;'>\g<0></a>", 
        text
    )

def dict_to_html(data) -> str:
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
        text_str = str(data)
        text_str = linkify_urls(text_str)
        return text_str

def parse_and_format_json_or_dict(content: str) -> str:
    try:
        if (content.strip().startswith("{") and content.strip().endswith("}")) or (content.strip().startswith("[") and content.strip().endswith("]")):
            data = ast.literal_eval(content)
            return dict_to_html(data)
    except:
        pass

    try:
        data = json.loads(content)
        return dict_to_html(data)
    except:
        pass

    return linkify_urls(content)

def display_message(role: str, content: str, iteration_count: int):
    markers = ["Thought:", "Action:", "Final Answer:", "Error:"]
    blocks = []
    
    pos = 0
    while pos < len(content):
        next_marker_pos = len(content)
        next_marker = None

        for m in markers:
            find_pos = content.find(m, pos)
            if find_pos != -1 and find_pos < next_marker_pos:
                next_marker_pos = find_pos
                next_marker = m

        if not next_marker:
            block_text = content[pos:].strip()
            if block_text:
                blocks.append(("default", block_text))
            break
        else:
            if next_marker_pos > pos:
                default_text = content[pos:next_marker_pos].strip()
                if default_text:
                    blocks.append(("default", default_text))

            start_of_block = next_marker_pos + len(next_marker)
            subsequent_marker_pos = len(content)
            for m in markers:
                find_pos = content.find(m, start_of_block)
                if find_pos != -1 and find_pos < subsequent_marker_pos:
                    subsequent_marker_pos = find_pos

            block_text = content[start_of_block:subsequent_marker_pos].strip()

            lower_marker = next_marker.lower()
            if "thought:" in lower_marker:
                block_type = "thought"
            elif "action:" in lower_marker:
                block_type = "action"
            elif "final answer:" in lower_marker:
                block_type = "final"
            elif "error:" in lower_marker:
                block_type = "error"
            else:
                block_type = "default"

            blocks.append((block_type, block_text))
            pos = subsequent_marker_pos

    def parse_and_clean(block_type, text):
        if block_type == "thought":
            # Handle multiple JSON objects in the response
            json_objects = re.findall(r'\{[^{}]*\}', text)
            
            for json_str in json_objects:
                try:
                    # Clean up Python None -> JSON null
                    json_str = json_str.replace(": None", ": null")
                    json_str = json_str.replace("'null'", "null")
                    json_str = json_str.replace('"None"', "null")
                    
                    data = json.loads(json_str)
                    
                    # First check for 'answer' field
                    if 'answer' in data:
                        return str(data['answer'])
                    # Then check for 'thought' field
                    elif 'thought' in data:
                        return str(data['thought'])
                except json.JSONDecodeError:
                    continue
            
            # If JSON parsing fails, try Python literal eval
            try:
                data = ast.literal_eval(text)
                if isinstance(data, dict):
                    if 'answer' in data:
                        return str(data['answer'])
                    elif 'thought' in data:
                        return str(data['thought'])
            except:
                pass

            # If all parsing fails, handle as markdown
            text = text.split('\n* **action**:')[0]
            text = re.sub(r'^\*\*thought\*\*:\s*', '', text, flags=re.IGNORECASE)
            return text.strip()
        elif block_type == "action":
            text = re.sub(r'^(action:\s*)', '', text, flags=re.IGNORECASE)
            text = text.replace("Name.", "")
            text = text.strip()
        elif block_type == "final":
            text = re.sub(r'^(final answer:\s*)', '', text, flags=re.IGNORECASE).strip()
        elif block_type == "error":
            text = re.sub(r'^(error:\s*)', '', text, flags=re.IGNORECASE).strip()

        return parse_and_format_json_or_dict(text)

    for (block_type, raw_text) in blocks:
        cleaned_html = parse_and_clean(block_type, raw_text)
        
        if block_type == "thought" and role == "assistant":
            with st.expander(f"Thought Process (Iteration {iteration_count})", expanded=False):
                thought_content = cleaned_html
                if isinstance(thought_content, str):
                    thought_content = thought_content.strip("'\"")  # Remove any quotes
                st.markdown(
                    f"""
                    <div style='
                        background-color:#E6EEFF; 
                        border-radius:8px; 
                        margin:10px 0; 
                        padding:15px; 
                        font-size:15px;
                        line-height:1.5;
                        color:#2C3E50;'
                    >
                        {thought_content}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        elif block_type == "action" and role == "assistant":
            with st.expander(f"Action (Iteration {iteration_count})", expanded=False):
                st.markdown(
                    f"""
                    <div style='
                        background-color:#F0E6FF; 
                        border-radius:8px; 
                        margin:10px 0; 
                        padding:10px; 
                        border-left:3px solid #555; 
                        font-size:14px;'
                    >
                        <strong style='color:#6C3483;'>Action:</strong> {cleaned_html}
                    </div>
                    """,
                    unsafe_allow_html=True
                )

        elif block_type == "final" and role == "assistant":
            st.markdown(
                f"""
                <div style='
                    background-color:#DFFFE3; 
                    border-radius:8px; 
                    margin:16px 0; 
                    padding:12px; 
                    font-size:15px;'
                >
                    <strong style='color:#186A3B;'>Final Answer:</strong> {cleaned_html}
                </div>
                """,
                unsafe_allow_html=True
            )

        elif block_type == "error":
            st.markdown(
                f"""
                <div style='
                    background-color:#FFCCCC; 
                    border-radius:8px; 
                    margin:10px 0; 
                    padding:10px; 
                    border:2px solid #AA0000; 
                    font-size:14px;'
                >
                    <strong style='color:#AA0000;'>Error:</strong> {cleaned_html}
                </div>
                """,
                unsafe_allow_html=True
            )

        else:
            st.markdown(
                f"""
                <div style='
                    background-color:#FFFFFF; 
                    border-radius:8px; 
                    margin:10px 0; 
                    padding:10px; 
                    font-size:14px;'
                >
                    <strong>{role.capitalize()}:</strong> {cleaned_html}
                </div>
                """,
                unsafe_allow_html=True
            )

def run():
    st.set_page_config(
        page_title="Agentic Search",
        layout="wide",
        page_icon="💡",
        initial_sidebar_state="expanded"
    )

    st.markdown(
        """
        <style>
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;700&family=Righteous&display=swap');

        html, body {
            font-family: 'Nunito Sans', 'Helvetica', sans-serif;
            font-size: 14px;
            background-color: #f8f8f8;
        }
        h1, h2, h3, h4 {
            font-family: 'Righteous', 'Cascadia Code', monospace;
            color: #222;
        }
        .main-title {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96C93D);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-size: 4rem;
            font-weight: 700;
            text-align: center;
            margin-bottom: 10px;
            font-family: 'Righteous', cursive;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            animation: gradient 5s ease infinite;
            background-size: 300% 300%;
        }
        .subtitle {
            font-size: 1.5rem;
            text-align: center;
            color: #666;
            margin-bottom: 30px;
            font-family: 'Inter', sans-serif;
            background: linear-gradient(120deg, #FF69B4, #4B0082);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
        }
        @keyframes gradient {
            0% { background-position: 0% 50%; }
            50% { background-position: 100% 50%; }
            100% { background-position: 0% 50%; }
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    with st.sidebar:
        if os.path.exists(GOOGLE_ICON_PATH):
            st.image(GOOGLE_ICON_PATH, width=40)

        max_iterations = st.number_input(
            "Max Iterations",
            min_value=1,
            max_value=20,
            value=3,
            step=1,
            help="Set how many reasoning steps the agent can perform."
        )

    st.markdown("<h1 class='main-title'>Agentic Search</h1>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Discover Insights Through AI-Powered Exploration</div>", unsafe_allow_html=True)

    user_query = st.text_input(
        "",
        key="explore_question",
        label_visibility="collapsed",
        placeholder="Ask anything...",
        help="Type your question here!"
    )
    search_clicked = st.button(
        "Explore",
        key="search_button",
        type="primary",
        help="Ask the Gemini React Agent"
    )

    if search_clicked and user_query.strip():
        st.markdown(
            """
            <h2 style='
                color: #9b59b6; 
                margin-top: 40px;
                margin-bottom: 5px;
            '>
                Reasoning Trace
            </h2>
            <hr style='border:none;border-top:1px solid #eee;margin-bottom: 20px;' />
            """,
            unsafe_allow_html=True
        )

        final_answer_collected = False

        for iteration_count, data in enumerate(
            run_react_agent(user_query, max_iterations), start=1
        ):
            for msg in data["messages"]:
                display_message(msg.role, msg.content, iteration_count)

                if "Final Answer:" in msg.content:
                    final_answer_collected = True

            if data.get("done") or (iteration_count == max_iterations):
                break

        if not final_answer_collected:
            st.markdown(
                """
                <div style='
                    background-color:#DFFFE3; 
                    border-radius:8px; 
                    margin:16px 0; 
                    padding:12px; 
                    font-size:15px;'
                >
                    <strong style='color:#186A3B;'>Final Answer:</strong>
                    (No explicit final answer was provided by the agent.)
                </div>
                """,
                unsafe_allow_html=True
            )

if __name__ == "__main__":
    run()