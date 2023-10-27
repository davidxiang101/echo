from transformers import BartForConditionalGeneration, BartTokenizer
import sys

sys.path.append("/Users/cactuscolada/Projects/echo")
from storage.storage_manager import StorageManager


def summarize_text(model, tokenizer, text):
    inputs = tokenizer([text], max_length=1024, return_tensors="pt", truncation=True)
    summary_ids = model.generate(
        inputs.input_ids,
        num_beams=4,
        min_length=30,
        max_length=100,
        early_stopping=True,
    )
    return [
        tokenizer.decode(
            g, skip_special_tokens=True, clean_up_tokenization_spaces=False
        )
        for g in summary_ids
    ]


def main():
    # Initialize BART model and tokenizer
    model = BartForConditionalGeneration.from_pretrained("facebook/bart-large-cnn")
    tokenizer = BartTokenizer.from_pretrained("facebook/bart-large-cnn")

    # Initialize storage manager and fetch articles
    storage_manager = StorageManager()
    articles = storage_manager.fetch_articles()

    for article_id, url, content in articles:
        # Generate summary
        summary = summarize_text(model, tokenizer, content)[0]

        print(f"URL: {url}")
        print(f"Summary: {summary}")

        # Update the database with the generated summary
        storage_manager.update_article_summary(article_id, summary)

    # Close the database connection
    storage_manager.close()


if __name__ == "__main__":
    main()
