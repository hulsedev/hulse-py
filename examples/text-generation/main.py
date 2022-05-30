from hulse import Hulse, settings

task = "text-generation"
model = "facebook/opt-125m"
data = "Hey, how are you?"

client = Hulse(api_key=settings.HULSE_API_KEY)
result = client.query(
    task=task,
    model=model,
    data=data,
)
print(result)
