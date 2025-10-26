# **Local Qwen3 LLM Project with Docker**

This project uses Docker and Docker Compose to run a local Qwen3 LLM (via Ollama) and query it with a separate Python script, also running in Docker.

## **Pre-requisites**

- You must have Docker installed and running. This projects aim is a quick development test to use Docker containers and Docker compose to run and query an LLM locally. [Download Docker](https://www.docker.com/)
- For this project you need an Nvidia GPU to use GPU processing for the LLM. Use the CPU folders if you do not have an Nvidia GPU and want to use CPU processing

## **Project Structure**

.  
├── client/  
│   ├── Dockerfile  
│   └── run_query.py  
├── docker-compose.yml  
└── README.md

* docker-compose.yml: Defines the Ollama LLM server and the Python client services.  
* client/Dockerfile: The build recipe for your Python client.  
* client/run_query.py: Your Python script that sends a question to the LLM.

## **Important: Note on GPU vs. CPU Usage**

By default, this project will run the LLM using your CPU. If you have an NVIDIA GPU, you can (and should) use it for a massive performance increase.

**To enable GPU support:**

Install the NVIDIA Container Toolkit: You must first install this on your host machine (your computer, not the container). 

Official Instructions: [NVIDIA Container Toolkit Install Guide](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)

**Configure the Docker Daemon:**

After installation, you must configure the Docker daemon to recognize the NVIDIA runtime. The toolkit provides a helper command for this:

> sudo nvidia-ctk runtime configure --runtime=docker

**Restart the Docker Daemon:**

For the new configuration to take effect, restart the Docker service:

> sudo systemctl restart docker

**Edit docker-compose.yml:**

After installing the toolkit, open the docker-compose.yml file and uncomment the deploy block under the ollama service.

## **Step-by-Step Instructions**

### **Step 1: Initial Setup (One-Time Only)**

Before you can run the query, you need to start the Ollama service and pull the Qwen3 model.

**Start the Ollama Service:**

Open your terminal in the project's root directory and run:

> docker-compose up -d ollama

This starts the Ollama server in the background.

**Pull the Qwen3 Model:**

While the server is running, execute the following command to download the qwen3:8b model. This model is a good balance of size and performance (\~5.2GB).
	
> docker-compose exec ollama ollama pull qwen3:8b
   
You only need to do this once.

You can replace qwen3:8b with other model tags like qwen3:4b if you prefer a smaller model.
   
### **Step 2: Run The Interactive Chat**

Now that the model is downloaded, you can run the interactive Python script.

> docker-compose up --build client

This command will: 

1. **Build** the client Docker image (if it's changed).  
2. **Start** the client container.  
3. **Run** the *run_query.py* script and attach the terminal to it, starting an interactive chat session.

You will see a welcome message and a You: prompt.

### **How to Use the Chat** 

* Simply type your question or prompt and press **Enter**.  
* The script will send your prompt to the LLM and print its response.  
* To quit the chat session, type exit or quit and press **Enter**.

### **Other Useful Commands**

**Stop all services:** 

(If the chat client is running, you may need to press Ctrl+C first or run this in a new terminal)

> docker-compose down

**View Ollama server logs:**

> docker-compose logs -f ollama

**Stop and remove the persistent model data:**

(This will delete the downloaded models.)

> docker-compose down -v
