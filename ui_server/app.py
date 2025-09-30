# # # app.py
# # import gradio as gr
# # from backend import send_topic_request, consume_article_ids, fetch_articles_by_ids, format_articles
# # from config import TOPICS

# # # --- יצירת UI ---
# # with gr.Blocks() as demo:
# #     with gr.Row():
# #         topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="בחר נושא")
# #     with gr.Row():
# #         output_area = gr.Markdown()

# # # --- פונקציית טיפול בבחירת נושא ---
# # def on_topic_change(topic):
# #     topic_name = TOPICS[topic]
# #     send_topic_request(topic_name)
# #     article_ids = consume_article_ids(topic_name)
# #     articles = fetch_articles_by_ids(article_ids)
# #     return format_articles(articles)

# # topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

# # # --- הפעלת השרת ---
# # if __name__ == "__main__":
# #     demo.launch(server_name="0.0.0.0", server_port=7860)

# # app.py
# import gradio as gr
# from backend import send_topic_request, consume_article_ids, fetch_articles_by_ids, format_articles
# from config import TOPICS

# # --- פונקציית טיפול בבחירת נושא ---
# def on_topic_change(topic):
#     topic_name = TOPICS[topic]
#     send_topic_request(topic_name)
#     article_ids = consume_article_ids(topic_name)
#     articles = fetch_articles_by_ids(article_ids)
#     return format_articles(articles)

# # --- יצירת UI ---
# with gr.Blocks() as demo:
#     with gr.Row():
#         topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="בחר נושא")
#     with gr.Row():
#         output_area = gr.Markdown()

#     # האירוע חייב להיות בתוך ה-Blocks
#     topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

# # --- הפעלת השרת ---
# if __name__ == "__main__":
#     demo.launch(server_name="0.0.0.0", server_port=7860)
# import gradio as gr
# from backend import send_topic_request, consume_article_ids, fetch_articles_by_ids, format_articles
# from config import TOPICS

# # --- פונקציית טיפול בבחירת נושא ---
# def on_topic_change(topic):
#     topic_name = TOPICS[topic]
#     send_topic_request(topic_name)
#     article_ids = consume_article_ids(topic_name)
#     articles = fetch_articles_by_ids(article_ids)
#     return format_articles(articles)

# # --- יצירת UI ---
# with gr.Blocks() as demo:
#     with gr.Row():
#         topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="בחר נושא")
#     with gr.Row():
#         output_area = gr.Markdown()

#     # האירוע חייב להיות בתוך ה-Blocks
#     topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

# # --- הפעלת השרת ---
# if __name__ == "__main__":
#     # שינינו ל-127.0.0.1 במקום 0.0.0.0
#     demo.launch(server_name="127.0.0.1", server_port=7860)
# app.py








import gradio as gr
from backend import consume_article_ids, fetch_articles_by_ids, format_articles
from config import TOPICS

# --- פונקציית טיפול בבחירת נושא ---
def on_topic_change(topic):
    topic_name = TOPICS[topic]
    # מקבלים IDs מ-Kafka
    article_ids = consume_article_ids(topic_name)
    print(article_ids)
    # שולפים כתבות מה-DB לפי IDs
    articles = fetch_articles_by_ids(article_ids)
  #  print(articles)
    # מחזירים לפורמט Markdown ל-Gradio
    return format_articles(articles)

# --- יצירת UI ב-Gradio ---
with gr.Blocks() as demo:
    with gr.Row():
        topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="בחר נושא")
    with gr.Row():
        output_area = gr.Markdown()

    # האירוע חייב להיות בתוך ה-Blocks
    topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

# --- הפעלת השרת על localhost ---
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)






















# import gradio as gr
# from backend import consume_article_ids, fetch_articles_by_ids
# from config import TOPICS
# from image import article_with_images

# # --- פונקציית טיפול בבחירת נושא ---
# def on_topic_change(topic):
#     topic_name = TOPICS[topic]
    
#     # מקבלים IDs מ-Kafka
#     article_ids = consume_article_ids(topic_name)
#     print("Article IDs:", article_ids)
    
#     # שולפים כתבות מה-DB לפי IDs
#     articles = fetch_articles_by_ids(article_ids)
    
#     # רשימה סופית עם טקסט + תמונה (או None)
#     result = []
#     for article in articles:
#         # שימוש ב-getattr במקום .get() כדי לתמוך ב-pyodbc.Row
#         content = getattr(article, "content", "")  # תוכן הכתבה
#         title = getattr(article, "title", "No Title")  # כותרת הכתבה
#         text, image_url = article_with_images(content)
#         result.append({
#             "title": title,
#             "text": text,
#             "image": image_url
#         })
    
#     # מחזירים רשימה ב‑Markdown או HTML
#     md_output = ""
#     for item in result:
#         md_output += f"### {item['title']}\n\n"
#         md_output += f"{item['text']}\n\n"
#         if item['image']:
#             md_output += f"![image]({item['image']})\n\n"
    
#     return md_output

# # --- יצירת UI ב-Gradio ---
# with gr.Blocks() as demo:
#     with gr.Row():
#         topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="בחר נושא")
#     with gr.Row():
#         output_area = gr.Markdown()

#     topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

# # --- הפעלת השרת על localhost ---
# if __name__ == "__main__":
#     demo.launch(server_name="127.0.0.1", server_port=7860)




























































#polling

# # app.py
# import gradio as gr
# from backend import consume_article_ids, fetch_articles_by_ids, format_articles
# from config import TOPICS

# # --- שמירה על המצב הקודם כדי לדעת אילו כתבות כבר הוצגו ---
# last_articles_cache = {topic: "" for topic in TOPICS.keys()}

# # --- Polling אוטומטי לכל הנושאים ---
# def live_update(_):
#     """
#     Polls all topics from Kafka, שולף כתבות חדשות מה-DB ומחזיר Markdown אחד משולב.
#     """
#     global last_articles_cache
#     combined_md = ""
#     for topic_key, topic_name in TOPICS.items():
#         article_ids = consume_article_ids(topic_name, timeout=500)  # Poll קצר
#         articles = fetch_articles_by_ids(article_ids)
#         md = format_articles(articles)

#         # רק אם יש שינויים
#         if md != last_articles_cache[topic_key]:
#             last_articles_cache[topic_key] = md
#         combined_md += f"## {topic_key}\n{last_articles_cache[topic_key]}\n\n"

#     return combined_md

# # --- יצירת UI ---
# with gr.Blocks() as demo:
#     output_area = gr.Markdown()

#     # Polling אוטומטי כל שנייה
#     live = gr.Live(fn=live_update, inputs=[], outputs=output_area, every=1)

# # --- הפעלת השרת על localhost ---
# if __name__ == "__main__":
#     demo.launch(server_name="127.0.0.1", server_port=7860)
