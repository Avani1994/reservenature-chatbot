## CHATBOT FOR RESERVENATURE

This work is for reservanture website - `https://reservenature.com/.` It's been in service since 2 years.
Their main goal is to be able to provide notify users via call or text whenever there are cancelleations for a campsite or permit. They give UI to users to create a tracker for their specified dates and camground/permit with other customizable parameters.

Currently they are using a commercial chat interface to help users who have difficult navigating the website, or who have questions about pricing plan, creating trackers or any other question in this domain.

Having the list of questions we saw many repetitive questions on different topics (trackers, subsciptions, availability, campsites etc.). Analysis has been done in `chatbotanalysis.md`

We though many repetitive questions could be handled by a chatbot. But how can we build one? 
LLMs to the rescue yay!

Either we could [finetune the LLM](https://en.wikipedia.org/wiki/Fine-tuning_(deep_learning)) using our own data or we could use [Retrieval Augmented Generation](https://arxiv.org/pdf/2312.10997.pdf)

For our usecase, ideally we are mostly answering questions based on factual information which is available on website faqs and how to pages. We are not changing the style or tone of the LLM generation. For example if we want to generate code, it would definitely need finetuning base model with code data. But for our use case we can fetch information from already available docs and resources. And this fetched information can be prompted to LLM to generate answer using the same style and tone as it has been trained for. Our usecase is typical usecase for Retrieval Augmentation Generation

We are using [Mistral Embeddings](https://docs.mistral.ai/guides/embeddings/) for text chunk representation and [faiss database](https://engineering.fb.com/2017/03/29/data-infrastructure/faiss-a-library-for-efficient-similarity-search/) as our vector datastore. Faiss allows efficient k nearest neighbor search for similar vectors.

## Prompting
We prompt LLM with retrieved context (top 3 most similar embedding with the question) and the question. We try few different Prompting Techniques:

1. Prompting with  - *Given the context information and not prior knowledge, answer the query.*. This makes sure LLM only answers with the given context and no prior knowledge it has been trained on but still remember style and theme/tone for answering
2. Prompting with - *Given the context information and not prior knowledge, answer the query. Please only answer the question if you have 95% confidence, other wise please say you don't know*. This makes LLM more restricted so that it doesnt answer anything which could be wrong. This technique is very helpful using RAGs which gives us a lot of control over what user sees. This is not possible with Finetuning

## Evaluation Techniques: [TODO]
<!-- We tried an evaluation Technique: -->


