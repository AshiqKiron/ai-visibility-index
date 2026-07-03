import time
import pandas as pd
from src.utils.config import QUERIES_FILE, MODELS, PROMPT_TEMPLATES
from src.utils.db_manager import init_db, save_citation
from src.parsers.url_extractor import extract_urls
from src.enrichers.authority_scorer import get_authority_score, get_freshness_days

# Import specific collectors (mocked here for structure)
# from src.collectors.chatgpt_collector import ChatGPTCollector

def run_experiment():
    init_db()
    
    # Load Queries
    df_queries = pd.read_csv(QUERIES_FILE)
    
    for _, row in df_queries.iterrows():
        topic = row['topic']
        category = row['category']
        
        for model_name in MODELS:
            for p_type, template in PROMPT_TEMPLATES.items():
                prompt = template.format(topic=topic)
                
                print(f"Running: {model_name} | {p_type} | {topic}")
                
                # --- MOCK RESPONSE GENERATION ---
                # In real code, replace this with: collector.query(prompt)
                # For demo, we generate fake URLs based on topic
                fake_urls = [
                    f"https://www.example-{topic.replace(' ', '')}.com/best-guide",
                    f"https://en.wikipedia.org/wiki/{topic}",
                    f"https://www.techcrunch.com/{topic}-review"
                ]
                
                # Simulate parsing
                for pos, url in enumerate(fake_urls):
                    domain = url.split("//")[-1].split("/")[0]
                    auth_score = get_authority_score(domain)
                    freshness = get_freshness_days(url)
                    
                    save_citation(
                        model=model_name,
                        query=topic,
                        prompt_type=p_type,
                        url=url,
                        domain=domain,
                        position=pos+1,
                        snippet=f"Snippet about {topic}...",
                        auth_score=auth_score,
                        freshness=freshness
                    )
                
                # Rate limiting to avoid bans
                time.sleep(2)

if __name__ == "__main__":
    run_experiment()