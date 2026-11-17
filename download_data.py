import pandas as pd
from datasets import load_dataset
print("Downloading 10000 real AI conversations... (This takes 3-4 minutes)")

# 1. Open the massive dataset in streaming mode
dataset = load_dataset("allenai/WildChat-1M", split="train", streaming=True)

# 2. Create empty lists (boxes) to hold our data
models = []
prompts = []
responses = []

# 3. Loop through the data one row at a time
count = 0
for row in dataset:
    if count >= 10000:
        break
        
    # Extract the conversation (it's a list of messages)
    conversation = row["conversation"]
    
    prompt_text = ""
    response_text = ""
    
    # Look inside the conversation for the first User and Assistant messages
    for msg in conversation:
        if msg["role"] == "user" and prompt_text == "":
            prompt_text = msg["content"]
        if msg["role"] == "assistant" and response_text == "":
            response_text = msg["content"]
            
    # If we found both, save them to our lists!
    if prompt_text != "" and response_text != "":
        models.append(row["model"])
        prompts.append(prompt_text)
        responses.append(response_text)
        count += 1
        
        if count % 2000 == 0:
            print(f"Downloaded {count} rows...")

# 4. Turn our lists into a Pandas DataFrame
df = pd.DataFrame({
    "model": models,
    "prompt": prompts,
    "response": responses
})

# 5. Save it as a CSV file
df.to_csv("real_data.csv", index=False)
print("Done! Saved 10000 rows to real_data.csv")