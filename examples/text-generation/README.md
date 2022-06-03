# Text Generation

Here is a simple example for running a text generation task with Hugging Face pipeline through Hulse. We demonstrate usage with the `facebook/opt-125m` text generation model.

## Getting Started

Refer to the instructions in the main `README.md` file for how to install hulse in your environment.

For the purpose of this example, you'll need to have a `.env` file available in your current directory, with the following variable specified:
```bash
HULSE_API_KEY="<your-hulse-api-key>"
```

Make sure that you have a running host in one of your Hulse clusters. If you're not sure you do, first check if you are part of any available clusters:
```bash
hulse login
hulse get-clusters
```

If you don't see any clusters listed, check out the `cluster-setup` example for instructions on how to setup one. If you're not sure whether someone in your clusters is already running a host, run one with the following command:

If nothing shows up, run a host on your local computer:
```bash
hulse host
```

Next, you can the `text-generation` example right away:
```bash
python3 main.py
```