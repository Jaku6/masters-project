# imports
import torch
from transformers import AutoTokenizer
from trl import PPOTrainer, PPOConfig, AutoModelForCausalLMWithValueHead, create_reference_model
from trl.core import respond_to_batch, LengthSampler
from tqdm import tqdm
import pandas as pd
from torch.utils.data import DataLoader, Dataset




class StringDataset(Dataset):
    def __init__(self, strings):
        self.strings = strings

    def __len__(self):
        return len(self.strings)

    def __getitem__(self, idx):
        return self.strings[idx]




tqdm.pandas()


my_dataset = StringDataset([
    "My favorite quote is the following: "
])



# get models
model = AutoModelForCausalLMWithValueHead.from_pretrained('gpt2')
model_ref = create_reference_model(model)

tokenizer = AutoTokenizer.from_pretrained('gpt2')
tokenizer.pad_token = tokenizer.eos_token

# initialize trainer
ppo_config = PPOConfig(
    seed=1,
    batch_size=1,
    ppo_epochs=3,
)

# create a ppo trainer
ppo_trainer = PPOTrainer(
    ppo_config,
    model,
    model_ref,
    tokenizer,
    dataset=my_dataset,
)

generation_kwargs = {
    "min_length": -1,
    "top_k": 0.0,
    "top_p": 1.0,
    "do_sample": True,
    "pad_token_id": tokenizer.eos_token_id,
    "max_new_tokens": 50,
    "batch_size": 1,
}


all_a_ratios = []


for epoch in range(1000):
    for batch in tqdm(ppo_trainer.dataloader):
        query_tensor = torch.tensor(tokenizer.encode(batch[0]), dtype=torch.long).long()

        # Get response from gpt2
        response_tensor = ppo_trainer.generate(query_tensor, return_prompt=False, **generation_kwargs).squeeze()

        # get plaintext so can calculate reward
        response = tokenizer.decode(response_tensor)


        #### Compute sentiment score
        # texts = [q + r for q, r in zip(batch["query"], batch["response"])]
        # pipe_outputs = sentiment_pipe(texts, **sent_kwargs)
        # rewards = [torch.tensor(output[1]["score"]) for output in pipe_outputs]
        a_ratio = response.count('a') / len(response)
        all_a_ratios.append(a_ratio)
        reward = torch.tensor(a_ratio, dtype=torch.float32).float()

        #### Run PPO step
        stats = ppo_trainer.step([query_tensor], [response_tensor], [reward])
        print(f'response: {response}')
        print(f'reward: {reward}')
        print('==============================')
        # ppo_trainer.log_stats(stats, batch, rewards)



print(all_a_ratios)



#
# # encode a query
# query_txt = "My favorite saying is as follows: "
# query_tensor = tokenizer.encode(query_txt, return_tensors="pt")
#
# # get model response
# response_tensor = respond_to_batch(model, query_tensor)
# print(f'response_tensor: {response_tensor}')
#
# # # create a ppo trainer
# # ppo_trainer = PPOTrainer(ppo_config, model, model_ref, tokenizer)
#
# # define a reward for response
# # (this could be any reward such as human feedback or output from another model)
# # reward = [torch.tensor(1.0)]
# # decoded_response = tokenizer.decode(response_tensor[0])
# # a_ratio = decoded_response.count('a') / len(decoded_response)
# # reward = [torch.tensor(a_ratio)]
#
# # train model for one step with ppo
# train_stats = ppo_trainer.step([query_tensor[0]], [response_tensor[0]], reward)