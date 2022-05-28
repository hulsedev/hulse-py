# hulse-py
Welcome to Hulse's Python Client! **Hulse is currently in beta.**

With your team's untapped computing power, Hulse makes self-hosting state-of-the-art open-source AI models easier.
Start reading below to learn how to use the Hulse API, and set up the Hulse desktop app.

If you have questions or want to talk about anything related to Hulse, you are welcome to join the community on [Discord](https://discord.gg/uPf74RXSC2)!

## Installation
hulse-py requires an active Hulse API key and a running Hulse cluster to run queries on AI models. Checkout the [Hulse Dashboard](https://hulse-api.herokuapp.com/login) to set these up. hulse-py supports Python 3.7+.

To install hulse-py:
```bash
pip install hulse
```

or from source, using this repository:
```bash
python setup.py install
```

## Getting Started

To get started, make sure you've retrieved your API key from [the dashboard](https://hulse-api.herokuapp.com/login). Here is a simple example of how to run queries using Hulse, and the [Hugging Face Transformers' pipeline](https://github.com/huggingface/transformers):
```python
import hulse

API_KEY = "<your-api-key>"
task = "text-classification"
# tweet https://twitter.com/GretaThunberg/status/1460159146720997377
data = "A reminder: the people in power don’t need conferences, treaties or agreements to start taking real climate action. They can start today. When enough people come together then change will come and we can achieve almost anything. So instead of looking for hope - start creating it."
client = hulse.Hulse()
client.query(task=task, data=data, api_key=API_KEY)
```
Here, we run a query using a `text-classification` model, which returns an estimation of the sentiment of the provided text. The provided data comes from [this tweet](https://twitter.com/GretaThunberg/status/1460159146720997377) from Greta Thunberg. 

## CLI Host
An alternative to using the macOS app is for you to run a Hulse host directly from your command line. This can be done using the Hulse CLI, and your API key:
```bash
hulse host --key="your-api-key"
```

To learn more, check out [Hulse Tutorials](https://sacha-levy.gitbook.io/hulse/), [Hulse Sphinx Docs](https://hulse-py.readthedocs.io/en/latest/?) or checkout the example folder for more information.