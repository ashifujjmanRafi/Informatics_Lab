# import numpy as np

# # Example responses from the LLM (1 for FORWARD, 0 for STOP)
# responses = [1] * 20  # 19 FORWARD + 1 FORWARD (counted as 1)

# # Calculate mean and variance
# mean_response = np.mean(responses)
# variance_response = np.var(responses)

# print("Mean:", mean_response)
# print("Variance:", variance_response)
import numpy as np
import matplotlib.pyplot as plt

# Response data (1 = FORWARD, 0 = STOP)
responses = [1] * 20  # All 20 responses were FORWARD

# Calculate statistics
mean_response = np.mean(responses)
variance_response = np.var(responses)
std_dev = np.std(responses)

# Create visualization
plt.figure(figsize=(8, 5))

# Bar plot for mean
plt.bar(['Mean'], [mean_response], color='skyblue', label=f'Mean: {mean_response:.2f}')

# Add error bar showing standard deviation
plt.errorbar(['Mean'], [mean_response], yerr=[std_dev], 
             fmt='none', ecolor='red', capsize=10, label=f'Std Dev: {std_dev:.2f}')

# Customize plot
plt.title('LLM Decision Tendency (FORWARD=1, STOP=0)', pad=20)
plt.ylim(0, 1.2)
plt.ylabel('Response Value')
plt.legend()
plt.grid(axis='y', alpha=0.3)

# Annotate important values
plt.text(0, mean_response+0.05, f'Variance: {variance_response:.2f}', 
         ha='center', va='bottom', fontsize=10)

plt.show()