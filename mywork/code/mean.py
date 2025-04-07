import numpy as np

# Example responses from the LLM (1 for FORWARD, 0 for STOP)
responses = [1] * 19 + [0]  # 19 FORWARD + 1 FORWARD (counted as 1)

# Calculate mean and variance
mean_response = np.mean(responses)
variance_response = np.var(responses)

print("Mean:", mean_response)
print("Variance:", variance_response)
