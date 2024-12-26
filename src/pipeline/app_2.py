from src.agents.react import run_react_agent
from src.config.setup import GOOGLE_ICON_PATH
from src.config.logging import logger
from typing import Optional
from typing import Tuple
from typing import List 
import streamlit as st
import requests
import ast
import os
import re
from pathlib import Path
import logging
from src.llm.gemini_text import generate_content

from src.config.client import initialize_genai_client
logger = logging.getLogger(__name__)

def extract_image_urls(text: str) -> list:
    """
    Enhanced function to extract both SERP API and regular image URLs from text.
    
    Matches:
    1. SerpAPI URLs: https://serpapi.com/searches/[ID]/images/[ID].[extension]
    2. Google encrypted image URLs: https://encrypted-tbn0.gstatic.com/images?q=[params]
    3. Regular image URLs: http(s)://domain/path/image.(jpg|jpeg|png|gif|webp)
    """
    # Pattern for serpapi image URLs
    serpapi_pattern = r'https:\/\/serpapi\.com\/searches\/[a-zA-Z0-9]+\/images\/[a-zA-Z0-9]+\.(?:jpeg|png|webp|jpg)'
    
    # Pattern for encrypted Google image URLs
    google_image_pattern = r'https:\/\/encrypted-tbn0\.gstatic\.com\/images\?q=[^"\s]+'
    
    # Pattern for regular image URLs
    regular_image_pattern = r'https?:\/\/(?!serpapi\.com|encrypted-tbn0\.gstatic\.com)[^\s<>"]+?\.(?:jpg|jpeg|png|gif|webp)(?:["\s]|$)'
    
    # Combine all patterns
    combined_pattern = f'({serpapi_pattern}|{google_image_pattern}|{regular_image_pattern})'
    
    # Find all matches
    matches = re.finditer(combined_pattern, text, re.IGNORECASE)
    
    # Extract unique URLs
    urls = []
    seen = set()
    
    for match in matches:
        url = match.group(0).strip('"\'[]() \t\n\r')  # Clean up URL
        if url not in seen:
            seen.add(url)
            urls.append(url)
            
    return urls



import re

def extract_and_clean_text(text: str) -> tuple[list[str], str]:
    """
    Extracts image URLs and cleans up the text by removing image references,
    including URLs with "URL:", "url:", and hyperlinks. Removes floating or broken brackets,
    HTTP/HTTPS URLs, patterns like [pattern] or (pattern), and adds breaklines for readability.
    """
    def extract_image_urls(text):
        # Define a regex pattern to extract valid URLs
        image_url_pattern = r'https?://[^\s\]\)]+'
        return re.findall(image_url_pattern, text)

    # Extract URLs using helper function
    urls = extract_image_urls(text)

    # Remove duplicates while maintaining order
    seen = set()
    urls = [url for url in urls if not (url in seen or seen.add(url))]
    
    # Clean the text
    processed_text = text
    
    # Remove patterns like [pattern] or (pattern)
    processed_text = re.sub(r'\[(.*?)\]', r'\1', processed_text)  # Remove square brackets
    processed_text = re.sub(r'\((.*?)\)', r'\1', processed_text)  # Remove parentheses
    
    # Remove broken or floating brackets
    processed_text = re.sub(r'\[', '', processed_text)  # Remove stray '['
    processed_text = re.sub(r'\]', '', processed_text)  # Remove stray ']'
    processed_text = re.sub(r'\(', '', processed_text)  # Remove stray '('
    processed_text = re.sub(r'\)', '', processed_text)  # Remove stray ')'
    
    # Remove HTTP/HTTPS URLs from the text
    processed_text = re.sub(r'https?://[^\s\]\)]+', '', processed_text)
    
    # Remove generic image references
    processed_text = re.sub(r'\[Image[^\]]*?\]', '', processed_text)
    
    # Remove URLs with "URL:", "url:" prefixes
    processed_text = re.sub(r'(URL|url):\s*\S+', '', processed_text)
    
    # Remove hyperlinks
    processed_text = re.sub(r'<a\s+href=[\'"]?([^\'" >]+)[\'"]?>.+?</a>', '', processed_text)
    
    # Add breaklines for readability
    processed_text = re.sub(r'(?<=[.!?]) ', '\n', processed_text)  # Add newline after end of sentences
    processed_text = re.sub(r'(?<=:)', '\n', processed_text)       # Add newline after colon

    # Clean up extra whitespace
    processed_text = re.sub(r'\s+', ' ', processed_text).strip()

    return urls, processed_text




def validate_image_url(url: str) -> bool:
    """Validates if a URL points to an accessible image."""
    try:
        response = requests.head(url, timeout=5)
        return (response.status_code == 200 and 
                'image' in response.headers.get('content-type', ''))
    except:
        return False

def render_image(url: str) -> str:
    """Renders an image with fallback handling."""
    is_valid = validate_image_url(url)
    if is_valid:
        return f"""<div style="margin:10px 0;">
                <img src="{url}" style="max-width:100%; border-radius:8px; box-shadow:0 2px 8px rgba(0,0,0,0.1);" 
                     onerror="this.style.display='none'; this.nextElementSibling.style.display='block';" />
                <div style="display:none; color:#666; font-size:13px; padding:10px; background:#f5f5f5; border-radius:4px;">
                    Image could not be loaded</div>
            </div>"""
    return f"""
        <div style="color:#666; font-size:13px; padding:10px; background:#f5f5f5; border-radius:4px;">
            Invalid image URL: {url}
        </div>
    """

def linkify_urls(text: str) -> str:
    """Converts URLs in text to clickable links."""
    url_pattern = re.compile(r"(http[s]?://\S+)")
    return url_pattern.sub(
        r"<a href='\g<0>' target='_blank' style='color: #1f77b4;'>\g<0></a>", 
        text
    )
    
def download_image(url: str) -> Optional[str]:
    """Downloads an image from a URL and saves it locally."""
    try:
        base_dir = Path('tmp/images')
        base_dir.mkdir(parents=True, exist_ok=True)
        filename = base_dir / f"{hash(url)}.jpg"
        
        if not filename.exists():
            response = requests.get(url, timeout=5)
            if response.status_code == 200:
                filename.write_bytes(response.content)
                logger.info(f"Successfully downloaded image to {filename}")
            else:
                logger.error(f"Failed to download image. Status code: {response.status_code}")
                return None
                
        return str(filename) if filename.exists() else None
    except Exception as e:
        logger.error(f"Error downloading image {url}: {str(e)}")
        return None

def parse_thought_action(text: str) -> tuple[str, str]:
    """Parses thought and action from agent response."""
    try:
        clean_text = text.replace("**Thought:**", "").replace("**Action:**", "").strip()
        data = ast.literal_eval(clean_text)
        if isinstance(data, dict):
            thought = data.get('thought', '')
            action = data.get('action', {})
            if isinstance(action, dict):
                action_str = f"Using {action.get('name', '')} tool\nReason: {action.get('reason', '')}\nInput: {action.get('input', '')}"
            else:
                action_str = str(action)
            return thought, action_str
    except:
        pass
    return text, text

def display_message(role: str, content: str, final_answer_container=None):
    """Displays a message with appropriate formatting and handles image extraction."""
    if not isinstance(content, str):
        try:
            content = str(content)
        except Exception as e:
            logger.error(f"Error converting content to string: {e}")
            content = "Error: Invalid message format"
            
    markers = ["Thought:", "Action:", "Final Answer:", "Error:"]
    blocks: List[Tuple[str, str]] = []
    
    pos = 0
    while pos < len(content):
        next_marker_pos = len(content)
        next_marker = None
        
        for m in markers:
            find_pos = content.find(m, pos)
            if find_pos != -1 and find_pos < next_marker_pos:
                next_marker_pos = find_pos
                next_marker = m
                
        if next_marker:
            if next_marker_pos > pos:
                block_text = content[pos:next_marker_pos].strip()
                if block_text:
                    blocks.append(("default", block_text))
                    
            block_end = len(content)
            for m in markers:
                next_pos = content.find(m, next_marker_pos + len(next_marker))
                if next_pos != -1 and next_pos < block_end:
                    block_end = next_pos
                    
            block_text = content[next_marker_pos + len(next_marker):block_end].strip()
            
            if next_marker.lower().startswith("thought"):
                thought_text, _ = parse_thought_action(block_text)
                block_text = thought_text
            elif next_marker.lower().startswith("action"):
                _, action_text = parse_thought_action(block_text)
                block_text = action_text
                
            block_type = next_marker.lower().replace(":", "")
            blocks.append((block_type, block_text))
            pos = block_end
        else:
            remaining = content[pos:].strip()
            if remaining:
                blocks.append(("default", remaining))
            break

    for block_type, text in blocks:
        if block_type == "final answer" and final_answer_container is not None:
            # Create separate containers for answer and images
            answer_container = final_answer_container.container()
            image_container = final_answer_container.container()
            
            # Extract URLs and clean text using our enhanced function
            all_urls, processed_text = extract_and_clean_text(text)
            
            # Process markdown formatting
            processed_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', processed_text)
            
            print('VVVVV')
            print(all_urls)
            print(processed_text)
            
            gemini_client = initialize_genai_client()

            MODEL_ID: str = "gemini-2.0-flash-exp"
            prompt: str = f"""
Clean and format it to nice markdown easy to read to the user - if there are images - say .. are shown below. 
Remove broken text and noise and make it professional. no fluff - no placeholders for images - 
no urls - no explanation of changes. 
be crisp and be aligned to the query\n\n{processed_text}\n strictly no placeholder for images like eg., Image 2 displayed below or [image] or [url] etc. """

            # Generate content
            response = generate_content(gemini_client, MODEL_ID, prompt).text
                
            # Display final answer first
            answer_container.markdown(
                f"""<div style='background-color:#FFFFFF; border-radius:12px; margin:24px 0; padding:30px; font-size:16px; line-height:1.8; color:#333; box-shadow:0 4px 12px rgba(0,0,0,0.05); border:1px solid #E0E0E0'>
                    <h3 style='color:#186A3B; margin:0 0 20px 0; font-size:24px; font-weight:600'>Final Answer</h3>
                    {response}""",
                unsafe_allow_html=True
            )

            # Handle and display images in a uniform grid
            if all_urls:
                # Create columns for the image grid - adjust number of columns as needed
                cols = image_container.columns(5)
                
                # Calculate image dimensions for uniform tiles
                image_width = 500  # Fixed width for all images
                image_height = 500  # Fixed height for all images
                
                # Iterate through URLs and display in grid
                for idx, url in enumerate(all_urls):
                    col_idx = idx % 6  # Determine which column to place the image
                    # Create a card-like container for each image
                    with cols[col_idx]:
                        st.markdown(
            f"""
            <div style="
                width: 100%; 
                display: flex; 
                justify-content: center; 
                align-items: center;  /* Center image vertically */
                overflow: hidden;   /* Hide any content that overflows */
                height: {image_height}px;  /* Set a fixed height for the container */
            "> 
                <img src="{url}" style="
                    width: {image_width}px; 
                    height: {image_height}px; 
                    object-fit: cover; 
                "> 
            </div>
            """,
            unsafe_allow_html=True
        )
                    
            

        # Style mapping for different block types
        style_map = {
            "thought": ("E6EEFF", "3498db", "Thought"),
            "action": ("F0E6FF", "6C3483", "Action"), 
            "error": ("FFCCCC", "AA0000", "Error"),
            "default": ("FFFFFF", "95a5a6", role.capitalize())
        }

        bg_color, accent_color, label = style_map.get(block_type, style_map["default"])
        
        st.markdown(
            f"""<div style='background-color:#{bg_color}; border-radius:8px; margin:10px 0; padding:15px; font-size:15px; line-height:1.5; color:#2C3E50; border-left:4px solid #{accent_color}'>
                <strong style='color:#{accent_color};'>{label}:</strong>
                <div style='margin-top:8px'>{text}</div>
            </div>""",
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
        .search-container {
            max-width: 800px;
            margin: 40px auto;
            padding: 20px;
            background: white;
            border-radius: 12px;
            box-shadow: 0 2px 8px rgba(0,0,0,0.05);
        }
        .stTextInput input {
            padding: 12px 20px;
            font-size: 16px;
            border: 2px solid #e1e1e1;
            border-radius: 8px;
            background: #f8f9fa;
            transition: all 0.3s ease;
        }
        .stTextInput input:focus {
            border-color: #4CAF50;
            box-shadow: 0 0 0 2px rgba(76,175,80,0.1);
            background: white;
        }
        .stButton button {
            padding: 12px 30px;
            font-size: 16px;
            font-weight: 500;
            border-radius: 8px;
            transition: all 0.3s ease;
            background: linear-gradient(45deg, #2196F3, #4CAF50);
            border: none;
            color: white;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        .stButton button:hover {
            transform: translateY(-1px);
            box-shadow: 0 4px 8px rgba(0,0,0,0.15);
        }
        .reasoning-title {
            background: linear-gradient(45deg, #FF6B6B, #4ECDC4, #45B7D1, #96C93D);
            -webkit-background-clip: text;
            background-clip: text;
            color: transparent;
            font-size: 4rem;
            font-weight: 700;
            text-align: left;
            margin-bottom: 10px;
            font-family: 'Righteous', cursive;
            text-shadow: 2px 2px 4px rgba(0,0,0,0.1);
            animation: gradient 5s ease infinite;
            background-size: 300% 300%;
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

    _, col2, _ = st.columns([6,2,6])
    with col2:
        search_clicked = st.button(
            "Explore",
            key="search_button",
            type="primary",
            help="Ask the Gemini React Agent"
        )

    if search_clicked and user_query.strip():
        final_answer_container = st.container()
        
        st.markdown(
            """
            <h2 class='reasoning-title'>
                Reasoning Trace
            </h2>
            """,
            unsafe_allow_html=True)

        for iteration_count, data in enumerate(
            run_react_agent(user_query, max_iterations), start=1
        ):
            st.markdown(
                f"""
                <div style='margin:24px 0 12px 0;'>
                    <span style='
                        color:#333;
                        font-size:14px;
                        font-weight:500;
                        text-transform:uppercase;
                        letter-spacing:0.5px;
                    '>
                        Iteration {iteration_count}
                    </span>
                </div>
                """,
                unsafe_allow_html=True
            )
            
            for msg in data["messages"]:
                display_message(msg.role, msg.content, final_answer_container)

            if data.get("done") or (iteration_count == max_iterations):
                break

if __name__ == "__main__":
    run()