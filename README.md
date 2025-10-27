# **Local Qwen3 LLM Project with Docker**

This project uses Docker and Docker Compose to run a local Qwen3 LLM (via Ollama) and query it with a separate Python script, also running in Docker.

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

**Enabling GPU Support (Host-Specific)**

Please follow the instructions for your operating system.

**If you are using Docker Desktop (Windows):**

The process is simple. You do not need to run any of the Linux commands.

1. Check Prerequisites:

	- NVIDIA Driver: Install the latest Game Ready or Studio Driver for your GPU from the NVIDIA website.
	- WSL 2: Ensure WSL 2 is installed. (Run wsl --install in an Admin PowerShell if needed).
	- Docker Desktop: Ensure it's configured to "Use the WSL 2 based engine" (this is the default). You can check this in Settings > General.

2. Edit docker-compose.yml: This is the only step. Open the docker-compose.yml file and uncomment the deploy block under the ollama service.

**If you are using a native Linux OS (e.g., Ubuntu):**

You must install the NVIDIA Container Toolkit and configure the Docker daemon. Install the NVIDIA Container Toolkit: You must first install this on your host machine (your computer, not the container). 

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

### **Step 1: Initial Setup**

Before you can run the query, you need to start the Ollama service and pull the Qwen3 model.

**Start the Ollama Service:**

Open your terminal in the project's root directory and run:

> docker-compose up -d ollama

This starts the Ollama server and will pull the latest Ollama image if necessary in the background.

**Pull the Qwen3 Model:**

While the server is running, execute the following command to download the qwen3:4b model. This model is a good balance of size and performance (~2.5GB). This should only need to be downloaded once as a volume is created to persist the downloaded models.
	
> docker-compose exec ollama ollama pull qwen3:4b
   
You only need to do this once.

You can replace qwen3:8b with other model tags like qwen3:4b if you prefer a smaller model.
   
### **Step 2: Run The Interactive Chat**

Now that the model is downloaded, you can run the interactive Python script.

> docker-compose run --build client

This command will: 

1. **Build** the client Docker image (if it's changed).  
2. **Start** the client container.  
3. **Run** the *run_query.py* script and attach your terminal to it, starting an interactive chat session.

You will see a welcome message and a You: prompt.

### **How to Use the Chat** 

* Simply type your question or prompt and press **Enter**.  
* The script will send your prompt to the LLM and print its response.  
* To quit the chat session, type exit or quit and press **Enter**.

### **Run The Interactive Chat Again After Initial Use**

To run the chat again if you quit and come back later, or you shutdown the Image, Containers or Docker Desktop:

Start the Ollama container:

> docker-compose up -d ollama

Run the interactive Python script.

> docker-compose run --build client

### **Other Useful Commands**

**Stop all services:** 

(If your chat client is running, you may need to press Ctrl+C first or run this in a new terminal)

> docker-compose down

**View Ollama server logs:**

> docker-compose logs -f ollama

**Stop and remove the persistent model data volume:**

THIS WILL DELETE THE DOWNLOADED MODELS

> docker-compose down -v

# **Troubleshooting:**

## **How to Verify GPU Usage**

If you suspect Ollama is using your CPU instead of your GPU, follow these steps.

**Check the Ollama Startup Logs**

1. Make sure the server is running (use docker-compose up -d ollama).
2. In a separate terminal, run this command to see the container's logs:

> docker logs ollama_server

Look at the output. You should see lines indicating it found the NVIDIA libraries. If it's successful, you'll see messages like adding compute level 6.1 or mentions of cuda. If it fails, you'll see errors about libnvidia-ml.so.1 not being found, followed by a message that it's falling back to CPU.
