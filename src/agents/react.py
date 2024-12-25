from src.tools.registry import get_google_trends_interest_over_time
from src.tools.registry import get_google_trends_compared_breakdown
from src.tools.registry import get_google_trends_interest_by_region
from src.tools.registry import get_google_finance_currency_exchange
from src.tools.registry import get_google_location_specific_search
from src.tools.registry import get_google_image_search_results
from src.tools.registry import get_google_finance_basic_search
from src.tools.registry import get_google_reverse_image_search
from src.tools.registry import get_google_events_basic_search
from src.tools.registry import get_google_videos_basic_search
from src.tools.registry import get_google_local_basic_search
from src.tools.registry import get_google_lens_basic_search
from src.tools.registry import get_google_play_query_search
from src.tools.registry import get_random_dog_breed_image
from src.tools.registry import get_google_shopping_search
from src.tools.registry import get_predicted_age_by_name
from src.tools.registry import get_google_search_results
from src.tools.registry import get_walmart_basic_search
from src.tools.registry import get_youtube_basic_search
from src.tools.registry import get_multiple_dog_images
from src.tools.registry import get_random_joke_by_type
from src.tools.registry import get_nationality_by_name
from src.tools.registry import get_wiki_search_results
from src.tools.registry import get_multiple_cat_facts
from src.config.client import initialize_genai_client
from src.tools.registry import get_google_news_search
from src.tools.registry import get_google_maps_search
from src.tools.registry import get_google_jobs_search
from src.tools.registry import get_google_maps_place
from src.tools.registry import get_random_dog_image
from src.tools.registry import get_ten_random_jokes
from src.tools.registry import get_random_fox_image
from src.tools.registry import get_trivia_questions
from src.tools.registry import get_gender_by_name
from src.tools.registry import get_exchange_rates
from src.llm.gemini_text import generate_content
from src.tools.registry import get_artwork_data
from src.tools.registry import get_iss_location
from src.tools.registry import get_random_joke
from src.tools.registry import get_cat_breeds
from src.tools.registry import get_public_ip
from src.tools.registry import get_cat_fact
from src.tools.registry import get_zip_info
from src.tools.registry import get_lyrics
from src.config.logging import logger
from src.utils.io import read_file
from pydantic import BaseModel
from typing import Callable
from typing import Union, List, Dict
from enum import Enum, auto
import json

Observation = Union[str, Exception]
PROMPT_TEMPLATE_PATH = "./templates/react.txt"

class Name(Enum):
    WIKI_SEARCH = auto()
    GOOGLE_SEARCH = auto()
    MULTIPLE_CAT_FACTS = auto()
    CAT_FACT = auto()
    CAT_BREEDS = auto()
    DOG_IMAGE = auto()
    MULTIPLE_DOG_IMAGES = auto()
    DOG_BREED_IMAGE = auto()
    RANDOM_JOKE = auto()
    TEN_RANDOM_JOKES = auto()
    RANDOM_JOKE_BY_TYPE = auto()
    PREDICT_AGE = auto()
    PREDICT_GENDER = auto()
    PREDICT_NATIONALITY = auto()
    ZIP_INFO = auto()
    PUBLIC_IP = auto()
    ARTWORK_DATA = auto()
    ISS_LOCATION = auto()
    LYRICS = auto()
    RANDOM_FOX_IMAGE = auto()
    TRIVIA_QUESTIONS = auto()
    EXCHANGE_RATES = auto()
    GOOGLE_IMAGE_SEARCH = auto()
    GOOGLE_NEWS_SEARCH = auto()
    GOOGLE_MAPS_SEARCH = auto()
    GOOGLE_MAPS_PLACE = auto()
    GOOGLE_JOBS_SEARCH = auto()
    GOOGLE_SHOPPING_SEARCH = auto()
    GOOGLE_TRENDS_INTEREST = auto()
    GOOGLE_TRENDS_BREAKDOWN = auto()
    GOOGLE_TRENDS_REGION = auto()
    GOOGLE_LENS_SEARCH = auto()
    GOOGLE_PLAY_SEARCH = auto()
    GOOGLE_LOCAL_SEARCH = auto()
    GOOGLE_EVENTS_SEARCH = auto()
    GOOGLE_VIDEOS_SEARCH = auto()
    GOOGLE_REVERSE_IMAGE_SEARCH = auto()
    GOOGLE_FINANCE_SEARCH = auto()
    GOOGLE_FINANCE_CURRENCY_EXCHANGE = auto()
    GOOGLE_LOCATION_SPECIFIC_SEARCH = auto()
    WALMART_SEARCH = auto()
    YOUTUBE_SEARCH = auto()
    NONE = "none"

class Tool:
    def __init__(self, name: Name, func: Callable[[str], str]):
        self.name = name
        self.func = func

    def use(self, query: str) -> Observation:
        try:
            return self.func(query)
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {e}")
            return str(e)

class Message(BaseModel):
    role: str
    content: str

class Agent:
    def __init__(self, model: str, max_iterations: int) -> None:
        self.model = model
        self.tools: Dict[Name, Tool] = {}
        self.messages: List[Message] = []
        self.query = ""
        self.max_iterations = max_iterations
        self.current_iteration = 0
        self.template = self.load_template()
        self.client = initialize_genai_client()

    def load_template(self) -> str:
        return read_file(PROMPT_TEMPLATE_PATH)

    def register_tool(self, name: Name, func: Callable[[str], str]) -> None:
        self.tools[name] = Tool(name, func)

    def trace(self, role: str, content: str) -> None:
        # Log to memory
        if role != "system":
            self.messages.append(Message(role=role, content=content))

    def get_history(self) -> str:
        return "\n".join(f"{m.role}: {m.content}" for m in self.messages)

    def ask_gemini(self, prompt: str) -> dict:
        response = generate_content(self.client, self.model, prompt)
        if response:
            response = str(response.text)
        else:
            response = 'No response from Gemini'

        cleaned_response = response.strip().strip('`').strip()
        if cleaned_response.startswith('json'):
            cleaned_response = cleaned_response[4:].strip()
        parsed_response = json.loads(cleaned_response)
        return parsed_response

    def think(self):
        # Start new iteration
        self.current_iteration += 1
        if self.current_iteration > self.max_iterations:
            self.trace("assistant",
                       "I'm sorry, but I couldn't find a satisfactory answer within the allowed number of iterations.")
            return None  # indicates done

        prompt = self.template.format(
            query=self.query,
            history=self.get_history(),
            tools=', '.join([str(t.name) for t in self.tools.values()])
        )

        # Get the LLM response
        response = self.ask_gemini(prompt)
        self.trace("assistant", f"Thought: {response}")
        return response

    def decide_and_act(self, response: dict):
        """
        Processes the agent's JSON response:
          {
            "action": {
               "name": "...",
               "input": "..."
            }
          }
          or
          {
            "answer": "final answer text..."
          }
        """
        try:
            if "action" in response:
                action = response["action"]
                name_str = action["name"].upper()
                if name_str == "NONE":
                    # Means no tool usage, let's continue to next iteration to produce final
                    return None
                else:
                    tool_name = Name[name_str]
                    self.trace("assistant", f"Action: Using {tool_name} tool")
                    query_input = action.get("input", self.query)
                    result = self.tools[tool_name].use(query_input)
                    # system observation
                    observation = f"Observation from {tool_name}: {result}"
                    self.trace("system", observation)
                    return None  # means keep going
            elif "answer" in response:
                # We got a final answer
                final = response["answer"]
                self.trace("assistant", f"Final Answer: {final}")
                return final
            else:
                raise ValueError("Unrecognized JSON structure")
        except Exception as e:
            logger.error(f"Error in decide_and_act: {e}")
            self.trace("assistant", "I encountered an error. Let me try again.")
            return None

    def run_iter(self, query: str):
        """
        This is a generator that yields data *only for the current iteration* 
        so we can display them in a separate panel in Streamlit.
        """
        self.query = query
        self.trace("user", query)

        final_answer = None

        while final_answer is None and self.current_iteration < self.max_iterations:
            response = self.think()
            if response is None:
                # means agent gave up or max iteration reached
                yield {
                    "iteration": self.current_iteration,
                    "messages": [],
                    "done": True,
                }
                break
                
            # Extract the messages generated only this iteration
            iteration_messages = []
            start_index = len(self.messages) - 1  # after we appended the "Thought"
            final_answer = self.decide_and_act(response)
            end_index = len(self.messages)

            # So new messages from this iteration are:
            iteration_messages = self.messages[start_index:end_index]

            yield {
                "iteration": self.current_iteration,
                "messages": iteration_messages,
                "done": (final_answer is not None)
            }

        yield {
            "iteration": self.current_iteration,
            "messages": [],
            "done": True,
        }


def build_agent(max_iterations: int) -> Agent:
    """
    Helper to instantiate an Agent, register all tools, and return it.
    """
    model = "gemini-2.0-flash-exp"
    agent = Agent(model=model, max_iterations=max_iterations)
    # Register your tools
    agent.register_tool(Name.WIKI_SEARCH, get_wiki_search_results)
    agent.register_tool(Name.GOOGLE_SEARCH, get_google_search_results)
    agent.register_tool(Name.CAT_FACT, get_cat_fact)
    agent.register_tool(Name.WALMART_SEARCH, get_walmart_basic_search)
    agent.register_tool(Name.MULTIPLE_CAT_FACTS, get_multiple_cat_facts)
    agent.register_tool(Name.CAT_BREEDS, get_cat_breeds)
    agent.register_tool(Name.DOG_IMAGE, get_random_dog_image)
    agent.register_tool(Name.MULTIPLE_DOG_IMAGES, get_multiple_dog_images)
    agent.register_tool(Name.DOG_BREED_IMAGE, get_random_dog_breed_image)
    agent.register_tool(Name.RANDOM_JOKE, get_random_joke)
    agent.register_tool(Name.TEN_RANDOM_JOKES, get_ten_random_jokes)
    agent.register_tool(Name.RANDOM_JOKE_BY_TYPE, get_random_joke_by_type)
    agent.register_tool(Name.PREDICT_AGE, get_predicted_age_by_name)
    agent.register_tool(Name.PREDICT_GENDER, get_gender_by_name)
    agent.register_tool(Name.PREDICT_NATIONALITY, get_nationality_by_name)
    agent.register_tool(Name.ZIP_INFO, get_zip_info)
    agent.register_tool(Name.PUBLIC_IP, get_public_ip)
    agent.register_tool(Name.ARTWORK_DATA, get_artwork_data)
    agent.register_tool(Name.ISS_LOCATION, get_iss_location)
    agent.register_tool(Name.LYRICS, get_lyrics)
    agent.register_tool(Name.RANDOM_FOX_IMAGE, get_random_fox_image)
    agent.register_tool(Name.TRIVIA_QUESTIONS, get_trivia_questions)
    agent.register_tool(Name.EXCHANGE_RATES, get_exchange_rates)
    agent.register_tool(Name.GOOGLE_IMAGE_SEARCH, get_google_image_search_results)
    agent.register_tool(Name.GOOGLE_NEWS_SEARCH, get_google_news_search)
    agent.register_tool(Name.GOOGLE_MAPS_SEARCH, get_google_maps_search)
    agent.register_tool(Name.GOOGLE_MAPS_PLACE, get_google_maps_place)
    agent.register_tool(Name.GOOGLE_JOBS_SEARCH, get_google_jobs_search)
    agent.register_tool(Name.GOOGLE_SHOPPING_SEARCH, get_google_shopping_search)
    agent.register_tool(Name.GOOGLE_TRENDS_INTEREST, get_google_trends_interest_over_time)
    agent.register_tool(Name.GOOGLE_TRENDS_BREAKDOWN, get_google_trends_compared_breakdown)
    agent.register_tool(Name.GOOGLE_TRENDS_REGION, get_google_trends_interest_by_region)
    agent.register_tool(Name.GOOGLE_LENS_SEARCH, get_google_lens_basic_search)
    agent.register_tool(Name.YOUTUBE_SEARCH, get_youtube_basic_search)
    agent.register_tool(Name.GOOGLE_PLAY_SEARCH, get_google_play_query_search)
    agent.register_tool(Name.GOOGLE_LOCAL_SEARCH, get_google_local_basic_search)
    agent.register_tool(Name.GOOGLE_VIDEOS_SEARCH, get_google_videos_basic_search)
    agent.register_tool(Name.GOOGLE_EVENTS_SEARCH, get_google_events_basic_search)
    agent.register_tool(Name.GOOGLE_REVERSE_IMAGE_SEARCH, get_google_reverse_image_search)
    agent.register_tool(Name.GOOGLE_FINANCE_SEARCH, get_google_finance_basic_search)
    agent.register_tool(Name.GOOGLE_FINANCE_CURRENCY_EXCHANGE, get_google_finance_currency_exchange)
    agent.register_tool(Name.GOOGLE_LOCATION_SPECIFIC_SEARCH, get_google_location_specific_search)

    return agent

def run_react_agent(query: str, max_iterations: int):
    """
    Returns a generator, which yields iteration data after each step.
    (This replaces the old run() that returned a single final answer.)
    """
    agent = build_agent(max_iterations=max_iterations)
    return agent.run_iter(query)