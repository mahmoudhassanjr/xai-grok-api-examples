# xAI API Examples
Following Grok 3's recent arrival to the XAI API, this is a repository for my personal use (based on XAI's documentation https://docs.x.ai/docs/overview#welcome) to quickly evaluate the capabilities of XAI's different Grok models and API functionality (e.g. streaming, function calling, etc). 

**Available Models**:
* Grok 3 mini fast
* Grok 3 mini
* Grok 3 fast
* Grok 3
* Grok 2 vision

**Included API Capabilities**:

* Chat
* Image understanding
* Streaming
* Parallelization
* Function calling

 **Installation Instructions**
 1. Clone the repository
 2. Install the requirements at the root of the project
    ```pip3 install -r requirements.txt```  
 3. Create a .env file at the root of the directory and add your XAI API key to it
    ```XAI_API_KEY=your-api-key```

**Running Instructions**
From here, you should be able to run any of the ```.py``` examples. Feel free to swap out the models in the examples with the appropriate models available under ```models.py```. 
