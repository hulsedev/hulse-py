# Text Generation

Here is a simple example for running a text generation task with Hugging Face pipeline through Hulse. We demonstrate usage with the `facebook/opt-125m` text generation model.

## Getting Started

Refer to the instructions in the main `README.md` file for how to install hulse in your environment. For this specific example, setup a `.env` file in the root of the `text-generation` folder, containing your Hulse api key:
```bash
HULSE_API_KEY=<your-api-key>
```

Make sure that you have a running host in one of your Hulse clusters. If you're not sure you do, first check if you are part of any available clusters:
```bash
hulse get-clusters --api-key=<your-api-key>
```

If you don't see any clusters listed, check out the `cluster-setup` example for instructions on how to setup one. 
Once you are part of a cluster, check if any host are running:
```bash
hulse get-hosts --api-key=<your-api-key>
```

If nothing shows up, run a host on your local computer:
```bash
hulse host --api-key=<your-api-key>
```

Next, you can the `text-generation` example right away:
```bash
python3 main.py
```