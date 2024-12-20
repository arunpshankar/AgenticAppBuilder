# AgenticAppBuilder

**A multi-agent framework that collaboratively ideates and constructs lightweight web applications, leveraging a curated set of public APIs, powered by Google Cloud Platform and Gemini.**

## Overview

AgenticAppBuilder is a cutting-edge framework designed to dynamically create lightweight web applications through multi-agent collaboration. Leveraging **Google Cloud Platform (GCP)** and **Gemini's advanced generative AI capabilities**, the framework intelligently ideates, delegates tasks, and seamlessly integrates APIs to deliver rapid and efficient application development.

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
- **GCP Account** with access to **Vertex AI** and **Cloud Run**
- **Docker** (optional, for containerized deployment)
- **Node.js** (for building web application frontends)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/<your-username>/AgenticAppBuilder.git
   cd AgenticAppBuilder
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up GCP credentials:
   - Download your GCP service account key file.
   - Set the `GOOGLE_APPLICATION_CREDENTIALS` environment variable:
     ```bash
     export GOOGLE_APPLICATION_CREDENTIALS="/path/to/your/key.json"
     ```

4. Set up `.env` for Gemini and API keys:
   Create a `.env` file in the root directory and add required keys:
   ```bash
   GEMINI_API_KEY=<Your-Gemini-API-Key>
   API_KEY_1=<Your-API-Key>
   ```

5. Run the application:
   ```bash
   python app.py
   ```

### GCP Deployment

For production use, deploy the application on GCP:

1. **Dockerize the application**:
   ```bash
   docker build -t gcr.io/<your-project-id>/agentic-app-builder .
   ```

2. **Push to Google Container Registry**:
   ```bash
   docker push gcr.io/<your-project-id>/agentic-app-builder
   ```

3. **Deploy to Cloud Run**:
   ```bash
   gcloud run deploy agentic-app-builder \
       --image gcr.io/<your-project-id>/agentic-app-builder \
       --platform managed \
       --region <your-region>
   ```

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

## Folder Structure

```
AgenticAppBuilder/
├── src/
│   ├── agents/
│   │   ├── coordinator.py
│   │   ├── frontend_agent.py
│   │   ├── backend_agent.py
│   │   └── testing_agent.py
│   ├── utils/
│   ├── templates/
│   └── app.py
├── data/
├── .env
├── requirements.txt
└── README.md
```

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




export PYTHONDONTWRITEBYTECODE=1
export PYTHONPATH=$PYTHONPATH:.