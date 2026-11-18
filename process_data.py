import pandas as pd
import tiktoken

print("Loading real data...")
df = pd.read_csv("real_data.csv")

# Load the tokenizer (the tool that counts tokens)
enc = tiktoken.get_encoding("cl100k_base")

# 1. Count tokens for prompt and response
print("Counting tokens...")
# lambda is just a quick, one-line function
df["prompt_tokens"] = df["prompt"].apply(lambda text: len(enc.encode(str(text))))
df["response_tokens"] = df["response"].apply(lambda text: len(enc.encode(str(text))))

# 2. Calculate the cost
# We create a dictionary (key-value pairs) for pricing per 1 million tokens
# NOTE: these are the standard list prices for gpt-3.5-turbo and gpt-4 (8k).
# The dataset contains the older snapshots gpt-3.5-turbo-0301 and gpt-4-0314,
# so costs are ESTIMATES based on these prices, not real billing data.
pricing = {
    "gpt-3.5-turbo": {"input": 0.50, "output": 1.50},
    "gpt-4": {"input": 30.00, "output": 60.00},
}

def calculate_cost(row):
    model = row["model"]

    # Check if the text "gpt-4" is inside the model name
    if "gpt-4" in model:
        model = "gpt-4"
    else:
        model = "gpt-3.5-turbo"

    p = pricing[model]

    # Math: (tokens / 1,000,000) * price
    input_cost = row["prompt_tokens"] * p["input"] / 1_000_000
    output_cost = row["response_tokens"] * p["output"] / 1_000_000
    return input_cost + output_cost

print("Calculating costs...")
# axis=1 tells pandas to give the function the ENTIRE row, not just one column
df["cost_usd"] = df.apply(calculate_cost, axis=1)

# 3. Flag as Useful or Waste
def is_useful(row):
    resp = str(row["response"]).lower().strip()

    # Rule 1: If the response OPENS with a refusal phrase, it's waste.
    # We only check the first 150 characters, because phrases like "as an AI"
    # can appear deep inside an otherwise helpful answer.
    refusal_phrases = ["i can't", "i cannot", "i'm sorry", "as an ai", "i am unable"]
    opening = resp[:150]
    for phrase in refusal_phrases:
        if phrase in opening:
            return False

    # Rule 2: If it's super short but the prompt was long, it's waste
    if row["response_tokens"] < 20 and row["prompt_tokens"] > 200:
        return False

    # If it passed the rules, it's useful!
    return True

print("Flagging useful vs waste...")
df["useful"] = df.apply(is_useful, axis=1)

# Save the results to a new file
df.to_csv("calls_clean.csv", index=False)
print("Done! Saved to calls_clean.csv")

# Print a quick summary
print("\n--- SUMMARY ---")
print(f"Total cost: ${df['cost_usd'].sum():.4f}")
# The ~ symbol means "NOT". So ~df['useful'] means rows where useful is False
print(f"Wasted spend: ${df.loc[~df['useful'], 'cost_usd'].sum():.4f}")
