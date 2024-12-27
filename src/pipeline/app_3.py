from src.config.client import initialize_genai_client
from src.llm.gemini_text import generate_content
from src.config.setup import GOOGLE_ICON_PATH
from src.utils.template import TemplateLoader
from src.agents.react import run_react_agent
from src.config.logging import logger
from typing import Optional
from typing import Tuple
from pathlib import Path
from typing import List 
import streamlit as st
import requests
import datetime
import base64
import ast
import os
import re


# Initialize template loader
template_loader = TemplateLoader()

def extract_image_urls_from_observation(observation: dict) -> list:
    """
    Extracts image URLs directly from the SerpAPI image search observation result.
    
    Args:
        observation (dict): The observation result from image_search tool
        
    Returns:
        list: List of extracted image URLs
    """
    image_urls = []
    print("Raw observation:", observation)  # Debug print
    
    try:
        # If observation is a string, try to parse it
        if isinstance(observation, str):
            try:
                observation = ast.literal_eval(observation)
            except:
                print("Failed to parse observation string")
                return image_urls
                
        if not isinstance(observation, dict):
            print(f"Invalid observation type after parsing: {type(observation)}")
            return image_urls
            
        # Traverse nested dictionaries to find image results
        if 'observation' in observation:
            observation = observation['observation']
        
        if isinstance(observation, str):
            try:
                observation = ast.literal_eval(observation)
            except:
                print("Failed to parse nested observation string")
                return image_urls
                
        # Look for image results in possible locations
        if 'image_results' in observation:
            results = observation['image_results']
        elif 'images_results' in observation:
            results = observation['images_results']
        elif 'inline_images' in observation:
            results = observation['inline_images']
        else:
            print("No recognized image results field found")
            print("Available keys:", observation.keys())
            return image_urls
            
        print("Found results array:", results)  # Debug print
            
        # Extract URLs from results
        for result in results:
            if isinstance(result, dict):
                # Try all possible URL fields
                for field in ['original', 'link', 'image', 'thumbnail', 'original_image']:
                    if field in result and result[field]:
                        url = result[field]
                        if isinstance(url, str) and url.startswith('http'):
                            image_urls.append(url)
                            break
                            
        print(f"Extracted {len(image_urls)} image URLs from observation")
        print("Extracted URLs:", image_urls)  # Debug print
                    
    except Exception as e:
        print(f"Error extracting image URLs from observation: {str(e)}")
        import traceback
        print("Traceback:", traceback.format_exc())
        
    return image_urls

def extract_image_urls(text: str) -> list:
    print(text, '<<' * 100)
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
        print(block_type, text, ')))))))')
        if block_type == "final answer" and final_answer_container is not None:
            # Create separate containers for answer and images
            answer_container = final_answer_container.container()
            image_container = final_answer_container.container()
            
            # Check if the text is a dict and might be an observation
            try:
                if isinstance(text, dict):
                    # Direct dictionary input
                    all_urls = extract_image_urls_from_observation(text)
                    processed_text = str(text)
                elif isinstance(text, str):
                    try:
                        # Try to parse as dictionary
                        observation = ast.literal_eval(text)
                        if isinstance(observation, dict):
                            # Successfully parsed as dictionary
                            all_urls = extract_image_urls_from_observation(observation)
                            processed_text = text
                        else:
                            # Not a valid observation dictionary
                            all_urls, processed_text = extract_and_clean_text(text)
                    except:
                        # Parsing failed, treat as normal text
                        all_urls, processed_text = extract_and_clean_text(text)
                else:
                    # Other type, convert to string
                    all_urls, processed_text = extract_and_clean_text(str(text))
            except Exception as e:
                print(f"Error in URL extraction: {e}")
                all_urls, processed_text = extract_and_clean_text(str(text))
            
            # Process markdown formatting
            processed_text = re.sub(r'\*\*(.*?)\*\*', r'<strong>\1</strong>', processed_text)
            
            print('VVVVV')
            print(all_urls)
            print(processed_text)
            
            gemini_client = initialize_genai_client()

            MODEL_ID: str = "gemini-2.0-flash-exp"
            prompt: str = f"""
Clean and format it to nice markdown (DO NOT use italics) easy to read to the user (escape dollar sign) - if there are images - say .. are shown below. 
Remove broken text and noise and make it professional. no fluff - no placeholders for images - 
no urls - no explanation of changes. 
be crisp and be aligned to the query\n\n{processed_text}\n strictly no placeholder for images like eg., Image 2 displayed below or [image] or [url] etc. DO NOT use italics in markdown."""

            # Generate content
            response = generate_content(gemini_client, MODEL_ID, prompt).text
            print(response, 'ppp' * 1000)
                
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
                                align-items: center;
                                overflow: hidden;
                                height: {image_height}px;
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

    # Load and inject templates
    st.markdown(template_loader.get_combined_styles(), unsafe_allow_html=True)

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

    # Create a container for the search components
    search_container = st.container()
    
    with search_container:
        st.markdown('<div class="search-wrapper">', unsafe_allow_html=True)
        
        # Main search input
        user_query = st.text_input(
            "Search or ask a question",
            key="explore_question",
            label_visibility="collapsed",
            placeholder="Ask anything...",
            help="Type your question here!"
        )
        
        # Hidden file uploader triggered by clip icon
        uploaded_file = st.file_uploader(
            "Upload Image",
            type=['png', 'jpg', 'jpeg'],
            key="hidden_uploader",
            label_visibility="collapsed"
        )
        
        # Clip icon and thumbnail display
        if uploaded_file is None:
            st.markdown(
                """
                <div class="clip-icon">
                    <svg xmlns="http://www.w3.org/2000/svg" width="24" height="24" viewBox="0 0 24 24" fill="none" 
                         stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round">
                        <path d="m21.44 11.05-9.19 9.19a6 6 0 0 1-8.49-8.49l8.57-8.57A4 4 0 1 1 18 8.84l-8.59 8.57a2 2 0 0 1-2.83-2.83l8.49-8.48"/>
                    </svg>
                </div>
                """,
                unsafe_allow_html=True
            )
        else:
            # Save the uploaded image
            if not os.path.exists('tmp/uploads'):
                os.makedirs('tmp/uploads', exist_ok=True)
            
            timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
            unique_id = abs(hash(uploaded_file.name))
            _, ext = os.path.splitext(uploaded_file.name)
            unique_filename = f"{timestamp}_{unique_id}{ext}"
            image_path = os.path.join('tmp/uploads', unique_filename)
                        
            with open(image_path, 'wb') as f:
                f.write(uploaded_file.getbuffer())
            
            # Log image upload
            logger.info(f"Image uploaded - Filename: {uploaded_file.name}, Saved as: {image_path}")
            
            # Display thumbnail and remove button
            st.markdown(
                f"""
                <div class="thumbnail-wrapper">
                    <img src="data:image/jpeg;base64,{base64.b64encode(uploaded_file.getvalue()).decode()}" 
                         class="thumbnail" alt="Uploaded image thumbnail"/>
                    <div class="remove-thumbnail">×</div>
                </div>
                """,
                unsafe_allow_html=True
            )
        
        st.markdown('</div>', unsafe_allow_html=True)

    # Center the Explore button
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
        
        # Prepare query with image if present
        if uploaded_file is not None:
            query_data = {
                "text": user_query,
                "image_path": image_path
            }
            # Log multimodal input
            logger.info(f"Multimodal input received - Query: {user_query}, Image: {image_path}")
        else:
            query_data = {
                "text": user_query,
                "image_path": None
            }
            # Log text-only input
            logger.info(f"Text-only input received - Query: {user_query}")

        st.markdown(
            """
            <h2 class='reasoning-title'>
                Reasoning Trace
            </h2>
            """,
            unsafe_allow_html=True
        )

        try:
            for iteration_count, data in enumerate(
                run_react_agent(query_data, max_iterations), start=1
            ):
                st.markdown(
                    f"""
                    <div style='margin:24px 0 12px 0;'>
                        <span style='color:#333; font-size:14px; font-weight:500; 
                               text-transform:uppercase; letter-spacing:0.5px;'>
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

        except Exception as e:
            st.error(f"An error occurred during processing: {str(e)}")
            logger.error(f"Error in run_react_agent: {str(e)}", exc_info=True)
        
        finally:
            # Cleanup uploaded image
            if uploaded_file is not None and os.path.exists(image_path):
                try:
                    os.remove(image_path)
                    logger.info(f"Cleaned up uploaded image: {image_path}")
                except Exception as e:
                    logger.error(f"Error cleaning up uploaded image: {str(e)}")

if __name__ == "__main__":
    run()