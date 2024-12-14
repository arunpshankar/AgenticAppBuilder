import time

def run_ideation():
    """
    Simulate an ideation process step-by-step, yielding logs as they occur.
    """
    steps = [
        "Initiating ideation process...",
        "Analyzing available APIs...",
        "Combining cat facts with weather data for a 'Cat Weather Trivia' idea...",
        "Generating code stubs...",
        "Finalizing ideas..."
    ]
    for step in steps:
        yield step
        time.sleep(1)

    # After completion, return a list of three mock ideas
    ideas = [
        {
            "title": "Cat Weather Trivia App",
            "description": "Displays cat facts alongside current weather info.",
            "apis_used": ["cat facts", "7timer!"]
        },
        {
            "title": "Dog Jokes in Your Area",
            "description": "Shows dog images and localized jokes based on ZIP code.",
            "apis_used": ["dog facts", "zip info", "jokes"]
        },
        {
            "title": "Geo Demographics Artist Insights",
            "description": "Presents art data filtered by nationality and age predictions.",
            "apis_used": ["age by name", "nationality by name", "art institute of chicago"]
        }
    ]
    return ideas
