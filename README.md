# hulse-py

Welcome to [Hulse](https://hulse.app)'s Python Client! **Hulse is currently in beta.**

With your team's untapped computing power, Hulse makes self-hosting state-of-the-art open-source AI models easier.
Start reading below to learn how to use the Hulse API, and set up the Hulse desktop app.

If you have questions or want to talk about anything related to Hulse, you are welcome to join the [discussion on Github](https://github.com/hulsedev/hulse-py/discussions)!

## Installation

To install hulse-py:
```bash
pip install hulse
```

or from source, using this repository:
```bash
git clone git@github.com:hulsedev/hulse-py.git
pip install -e .
```

## Setting Up

To run the example below, you'll need an active Hulse API key, to be part of a Hulse cluster, and at least one running host in your cluster. If you're not sure whether you have these three things setup, follow these steps:
```bash
hulse login
hulse create-cluster --name=<your-cluster-name> --description=<your-cluster-description>
hulse host
```
> An alternative to running the host from the CLI is to download the macOS app (currently only available for intel based platforms) from the [dashboard](https://hulse-api.herokuapp.com/login). You may also manage your clusters and API key there.

## Getting Started

At this stage, make sure you've retrieved **your API key** either using the CLI by running `hulse get-api-key` or from the [dashboard](https://hulse-api.herokuapp.com/login).

Here is a simple example of how to run queries using Hulse, and the [Hugging Face Transformers' pipeline](https://github.com/huggingface/transformers):
```python
import hulse

API_KEY = "<your-api-key>"
task = "text-classification"
# tweet https://twitter.com/GretaThunberg/status/1460159146720997377
data = "A reminder: the people in power don’t need conferences, treaties or agreements to start taking real climate action. They can start today. When enough people come together then change will come and we can achieve almost anything. So instead of looking for hope - start creating it."
client = hulse.Hulse(api_key=API_KEY)
client.query(task=task, data=data)
```

Here, we run a query using a `text-classification` model, which gives a prediction of the text's sentiment. The provided data comes from [this tweet](https://twitter.com/GretaThunberg/status/1460159146720997377) from Greta Thunberg. 

## Learn more

- [Hulse Tutorials](https://sacha-levy.gitbook.io/hulse/)
- [hulse-py Docs](https://hulsedev.github.io/hulse-py/)
- the example folder for more information
