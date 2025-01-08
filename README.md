# AgenticAppBuilder

**A multi-agent framework that collaboratively ideates and constructs lightweight web applications, leveraging a curated set of public APIs, powered by Google Cloud Platform and Gemini.**

![Agentic Search Overview](./img/agentic-app-builder.png)

## Overview

AgenticAppBuilder is an agentic framework designed to dynamically create lightweight web applications through multi-agent collaboration. Leveraging **Google Cloud Platform (GCP)** and **Gemini's advanced generative AI capabilities**, the framework intelligently ideates, delegates tasks, and seamlessly integrates APIs to deliver rapid and efficient application development.

## Features

- **Powered by GCP**: Scalable infrastructure with seamless deployment and integration of GCP services like **Cloud Functions**, **Vertex AI**, and **Cloud Run**.
- **Gemini Integration**: Uses Gemini for natural language understanding, code generation, and task orchestration.
- **Multi-Agent Collaboration**: Intelligent agents collaborate on frontend, backend, and testing tasks.
- **Curated API Library**: Includes a preselected set of high-quality public APIs.
- **Lightweight Applications**: Builds minimal, scalable, and efficient web tools.
- **Extensible Design**: Easily integrate additional APIs or extend agent capabilities to suit specific needs.

## Use Cases

- Rapid prototyping of web applications.
- Automating the ideation and creation of lightweight tools.
- Enhancing application design with AI-driven agent collaboration.
- Education and exploration of multi-agent frameworks.

## Getting Started

### Prerequisites

- **Python** 3.8 or higher

#### Getting API Keys

To utilize certain features, you'll need API keys from Gemini and SerpApi.

#### Gemini API Key

1. **Sign in to your Google Account**: Ensure you're logged in to your Google account.

2. **Access Google AI Studio**: Navigate to [Google AI Studio](https://ai.google.dev/aistudio).

3. **Obtain API Key**:
   - Click on the **"Gemini API"** tab.
   - Click the **"Get API Key in Google AI Studio"** button.
   - Review and accept the terms of service.
   - Choose to create the API key in a new or existing project.
   - Your API key will be generated; store it securely.

For detailed instructions, refer to [Google's official guide](https://ai.google.dev/gemini-api/docs/api-key).

#### SerpApi API Key

1. **Create an Account**: Sign up at [SerpApi](https://serpapi.com/users/sign_up).

2. **Access Dashboard**: After logging in, go to the [dashboard](https://serpapi.com/dashboard).

3. **Retrieve API Key**: Your private API key is displayed in the **"Your Private API Key"** section. Copy and store it securely.

For more information, visit [SerpApi's documentation](https://serpapi.com/search-api).

### Installation

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/arunpshankar/AgenticAppBuilder.git
   cd AgenticAppBuilder
   ```

2. **Create and Activate a Virtual Environment**:
   - **Create**:
     ```bash
     python -m venv venv
     ```
   - **Activate**:
     - **Windows**:
       ```bash
       venv\Scripts\activate
       ```
     - **macOS and Linux**:
       ```bash
       source venv/bin/activate
       ```

3. **Upgrade pip**:
   ```bash
   pip install --upgrade pip
   ```

4. **Install Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

5. **Set Environment Variables**:
   ```bash
   export PYTHONDONTWRITEBYTECODE=1
   export PYTHONPATH=$PYTHONPATH:.
   ```

6. **Configure API Keys**:
   - Create a folder named `credentials` inside the cloned project:
     ```bash
     mkdir credentials
     ```
   - Inside the `credentials` folder, create a YAML file named `api.yml` with the following content:
     ```yaml
     GOOGLE_API_KEY: your_gemini_api_key
     SERP_API_KEY: your_serpapi_api_key
     ```
   Replace `your_gemini_api_key` and `your_serpapi_api_key` with the API keys you obtained earlier.

7. **Run the Application**:
   ```bash
   streamlit run src/workflow/app.py
   ```

By following these steps, you'll set up the AgenticAppBuilder project with the necessary configurations and API integrations. 


### Demo

[Insert GIF or screenshots of the application workflow, including deployment on GCP]

## Usage

1. **Define Requirements**: Specify the application type and required features.
2. **Agent Collaboration**: Agents ideate and delegate tasks for frontend, backend, and API integration.
3. **Gemini Assistance**: Gemini provides natural language insights, code generation, and content refinement.
4. **Application Assembly**: The framework assembles the components into a cohesive application.
5. **Deploy on GCP**: Leverage GCP for production-grade scalability.

## Architecture

The framework leverages a multi-agent architecture powered by GCP and Gemini:

- **Coordinator Agent**: Detects intent and delegates tasks to specialized agents.
- **Frontend Agent**: Designs and develops the web interface.
- **Backend Agent**: Implements server-side logic and API integrations.
- **Testing Agent**: Validates the application’s functionality.
- **GCP Services**: Orchestrates and deploys the application on Cloud Run, Vertex AI, and other GCP tools.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a new branch: `git checkout -b feature-name`.
3. Commit your changes: `git commit -m 'Add new feature'`.
4. Push to the branch: `git push origin feature-name`.
5. Submit a pull request.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Contact

For queries or collaborations, please contact [Your Name](mailto:arunpshankar@google.com).
