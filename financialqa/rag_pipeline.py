# financialqa/rag_pipeline.py
from langchain.chains import RetrievalQA
from langchain_huggingface import HuggingFacePipeline
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

class RAGPipeline:
    def __init__(self, retriever, model_name="EleutherAI/gpt-neo-2.7B"):
        print(f"Loading GPT-Neo model: {model_name}...")
        tokenizer = AutoTokenizer.from_pretrained(model_name)
        model = AutoModelForCausalLM.from_pretrained(model_name)
        text_gen = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            device=0 if model.device.type == "cuda" else -1,
            max_new_tokens=100,
            do_sample=True,
            temperature=0.7,
            top_p=0.9
        )
        self.llm = HuggingFacePipeline(pipeline=text_gen)
        self.qa_chain = RetrievalQA.from_chain_type(llm=self.llm, retriever=retriever)

    def run_retrieval_qa(self, query: str):
        return self.qa_chain.invoke(query)
