import json
import os

from hulse import Hulse, settings

task = "text-generation"
model = "facebook/opt-125m"
data = "Hey, how are you?"

client = Hulse(api_key=os.getenv("HULSE_API_KEY"))
result = client.query(
    task=task,
    model=model,
    data=data,
)
print(json.dumps(result, indent=4))
