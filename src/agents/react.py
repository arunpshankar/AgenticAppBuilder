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
from src.utils.io import write_to_file
from src.config.logging import logger
from src.utils.io import read_file
from pydantic import BaseModel
from typing import Callable
from pydantic import Field 
from typing import Union
from typing import List 
from typing import Dict 
from enum import Enum
from enum import auto
import json


Observation = Union[str, Exception]

PROMPT_TEMPLATE_PATH = "./templates/react.txt"
OUTPUT_TRACE_PATH = "./data/trace.txt"

class Name(Enum):
    """
    Enumeration for tool names available to the agent.
    """
    WIKIPEDIA = auto()
    GOOGLE = auto()
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


class Choice(BaseModel):
    """
    Represents a choice of tool with a reason for selection.
    """
    name: Name = Field(..., description="The name of the tool chosen.")
    reason: str = Field(..., description="The reason for choosing this tool.")


class Message(BaseModel):
    """
    Represents a message with sender role and content.
    """
    role: str = Field(..., description="The role of the message sender.")
    content: str = Field(..., description="The content of the message.")


class Tool:
    """
    A wrapper class for tools used by the agent, executing a function based on tool type.
    """

    def __init__(self, name: Name, func: Callable[[str], str]):
        """
        Initializes a Tool with a name and an associated function.
        
        Args:
            name (Name): The name of the tool.
            func (Callable[[str], str]): The function associated with the tool.
        """
        self.name = name
        self.func = func

    def use(self, query: str) -> Observation:
        """
        Executes the tool's function with the provided query.

        Args:
            query (str): The input query for the tool.

        Returns:
            Observation: Result of the tool's function or an error message if an exception occurs.
        """
        try:
            return self.func(query)
        except Exception as e:
            logger.error(f"Error executing tool {self.name}: {e}")
            return str(e)


class Agent:
    """
    Defines the agent responsible for executing queries and handling tool interactions.
    """

    def __init__(self, model: str) -> None:
        """
        Initializes the Agent with a generative model, tools dictionary, and a messages log.

        Args:
            model (str): The generative model used by the agent.
        """
        self.model = model
        self.tools: Dict[Name, Tool] = {}
        self.messages: List[Message] = []
        self.query = ""
        self.max_iterations = 5
        self.current_iteration = 0
        self.template = self.load_template()
        self.client = initialize_genai_client()

    def load_template(self) -> str:
        """
        Loads the prompt template from a file.

        Returns:
            str: The content of the prompt template file.
        """
        return read_file(PROMPT_TEMPLATE_PATH)

    def register(self, name: Name, func: Callable[[str], str]) -> None:
        """
        Registers a tool to the agent.

        Args:
            name (Name): The name of the tool.
            func (Callable[[str], str]): The function associated with the tool.
        """
        self.tools[name] = Tool(name, func)

    def trace(self, role: str, content: str) -> None:
        """
        Logs the message with the specified role and content and writes to file.

        Args:
            role (str): The role of the message sender.
            content (str): The content of the message.
        """
        if role != "system":
            self.messages.append(Message(role=role, content=content))
        write_to_file(path=OUTPUT_TRACE_PATH, content=f"{role}: {content}\n")

    def get_history(self) -> str:
        """
        Retrieves the conversation history.

        Returns:
            str: Formatted history of messages.
        """
        return "\n".join([f"{message.role}: {message.content}" for message in self.messages])

    def think(self) -> None:
        """
        Processes the current query, decides actions, and iterates until a solution or max iteration limit is reached.
        """
        self.current_iteration += 1
        logger.info(f"Starting iteration {self.current_iteration}")
        write_to_file(path=OUTPUT_TRACE_PATH, content=f"\n{'='*50}\nIteration {self.current_iteration}\n{'='*50}\n")

        if self.current_iteration > self.max_iterations:
            logger.warning("Reached maximum iterations. Stopping.")
            self.trace("assistant", "I'm sorry, but I couldn't find a satisfactory answer within the allowed number of iterations. Here's what I know so far: " + self.get_history())
            return

        prompt = self.template.format(
            query=self.query, 
            history=self.get_history(),
            tools=', '.join([str(tool.name) for tool in self.tools.values()])
        )

        response = self.ask_gemini(prompt)
        logger.info(f"Thinking => {response}")
        self.trace("assistant", f"Thought: {response}")
        self.decide(response)

    def decide(self, response: str) -> None:
        """
        Processes the agent's response, deciding actions or final answers.

        Args:
            response (str): The response generated by the model.
        """
        try:
            cleaned_response = response.strip().strip('`').strip()
            if cleaned_response.startswith('json'):
                cleaned_response = cleaned_response[4:].strip()
            
            parsed_response = json.loads(cleaned_response)
            
            if "action" in parsed_response:
                action = parsed_response["action"]
                tool_name = Name[action["name"].upper()]
                if tool_name == Name.NONE:
                    logger.info("No action needed. Proceeding to final answer.")
                    self.think()
                else:
                    self.trace("assistant", f"Action: Using {tool_name} tool")
                    self.act(tool_name, action.get("input", self.query))
            elif "answer" in parsed_response:
                self.trace("assistant", f"Final Answer: {parsed_response['answer']}")
            else:
                raise ValueError("Invalid response format")
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse response: {response}. Error: {str(e)}")
            self.trace("assistant", "I encountered an error in processing. Let me try again.")
            self.think()
        except Exception as e:
            logger.error(f"Error processing response: {str(e)}")
            self.trace("assistant", "I encountered an unexpected error. Let me try a different approach.")
            self.think()

    def act(self, tool_name: Name, query: str) -> None:
        """
        Executes the specified tool's function on the query and logs the result.

        Args:
            tool_name (Name): The tool to be used.
            query (str): The query for the tool.
        """
        tool = self.tools.get(tool_name)
        if tool:
            result = tool.use(query)
            observation = f"Observation from {tool_name}: {result}"
            self.trace("system", observation)
            self.messages.append(Message(role="system", content=observation))  # Add observation to message history
            self.think()
        else:
            logger.error(f"No tool registered for choice: {tool_name}")
            self.trace("system", f"Error: Tool {tool_name} not found")
            self.think()

    def execute(self, query: str) -> str:
        """
        Executes the agent's query-processing workflow.

        Args:
            query (str): The query to be processed.

        Returns:
            str: The final answer or last recorded message content.
        """
        self.query = query
        self.trace(role="user", content=query)
        self.think()
        return self.messages[-1].content

    def ask_gemini(self, prompt: str) -> str:
        """
        Queries the generative model with a prompt.

        Args:
            prompt (str): The prompt text for the model.

        Returns:
            str: The model's response as a string.
        """
        response = generate_content(self.client, self.model, prompt)
        return str(response) if response is not None else "No response from Gemini"

def run(query: str) -> str:
    """
    Sets up the agent, registers tools, and executes a query.

    Args:
        query (str): The query to execute.

    Returns:
        str: The agent's final answer.
    """
    model = "gemini-2.0-flash-exp"
    agent = Agent(model=model)
    agent.register(Name.WIKIPEDIA, get_wiki_search_results)
    agent.register(Name.GOOGLE, get_google_search_results)
    agent.register(Name.CAT_FACT, get_cat_fact)
    agent.register(Name.WALMART_SEARCH, get_walmart_basic_search)
    agent.register(Name.MULTIPLE_CAT_FACTS, get_multiple_cat_facts)
    agent.register(Name.CAT_BREEDS, get_cat_breeds)
    agent.register(Name.DOG_IMAGE, get_random_dog_image)
    agent.register(Name.MULTIPLE_DOG_IMAGES, get_multiple_dog_images)
    agent.register(Name.DOG_BREED_IMAGE, get_random_dog_breed_image)
    agent.register(Name.RANDOM_JOKE, get_random_joke)
    agent.register(Name.TEN_RANDOM_JOKES, get_ten_random_jokes)
    agent.register(Name.RANDOM_JOKE_BY_TYPE, get_random_joke_by_type)
    agent.register(Name.PREDICT_AGE, get_predicted_age_by_name)
    agent.register(Name.PREDICT_GENDER, get_gender_by_name)
    agent.register(Name.PREDICT_NATIONALITY, get_nationality_by_name)
    agent.register(Name.ZIP_INFO, get_zip_info)
    agent.register(Name.PUBLIC_IP, get_public_ip)
    agent.register(Name.ARTWORK_DATA, get_artwork_data)
    agent.register(Name.ISS_LOCATION, get_iss_location)
    agent.register(Name.LYRICS, get_lyrics)
    agent.register(Name.RANDOM_FOX_IMAGE, get_random_fox_image)
    agent.register(Name.TRIVIA_QUESTIONS, get_trivia_questions)
    agent.register(Name.EXCHANGE_RATES, get_exchange_rates)
    agent.register(Name.GOOGLE_IMAGE_SEARCH, get_google_image_search_results)
    agent.register(Name.GOOGLE_NEWS_SEARCH, get_google_news_search)
    agent.register(Name.GOOGLE_MAPS_SEARCH, get_google_maps_search)
    agent.register(Name.GOOGLE_MAPS_PLACE, get_google_maps_place)
    agent.register(Name.GOOGLE_JOBS_SEARCH, get_google_jobs_search)
    agent.register(Name.GOOGLE_SHOPPING_SEARCH, get_google_shopping_search)
    agent.register(Name.GOOGLE_TRENDS_INTEREST, get_google_trends_interest_over_time)
    agent.register(Name.GOOGLE_TRENDS_BREAKDOWN, get_google_trends_compared_breakdown)
    agent.register(Name.GOOGLE_TRENDS_REGION, get_google_trends_interest_by_region)
    agent.register(Name.GOOGLE_LENS_SEARCH, get_google_lens_basic_search)
    agent.register(Name.YOUTUBE_SEARCH, get_youtube_basic_search)
    agent.register(Name.GOOGLE_PLAY_SEARCH, get_google_play_query_search)
    agent.register(Name.GOOGLE_LOCAL_SEARCH, get_google_local_basic_search)
    agent.register(Name.GOOGLE_VIDEOS_SEARCH, get_google_videos_basic_search)
    agent.register(Name.GOOGLE_EVENTS_SEARCH, get_google_events_basic_search)
    agent.register(Name.GOOGLE_REVERSE_IMAGE_SEARCH, get_google_reverse_image_search)
    agent.register(Name.GOOGLE_FINANCE_SEARCH, get_google_finance_basic_search)
    agent.register(Name.GOOGLE_FINANCE_CURRENCY_EXCHANGE, get_google_finance_currency_exchange)
    agent.register(Name.GOOGLE_LOCATION_SPECIFIC_SEARCH, get_google_location_specific_search)
    answer = agent.execute(query)
    return answer


if __name__ == "__main__":
    query = "What is the age of the oldest tree in the country that has won the most FIFA World Cup titles?"
    final_answer = run(query)
    logger.info(final_answer)
    