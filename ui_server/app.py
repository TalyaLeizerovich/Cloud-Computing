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

# # --- פונקציית טיפול בבחירת נושא ---
# def on_topic_change(topic):
#     topic_name = TOPICS[topic]
    
#     # מקבלים IDs מ-Kafka
#     article_ids = consume_article_ids(topic_name)
#     print("Article IDs:", article_ids)
    
#     # שולפים כתבות מה-DB לפי IDs
#     articles = fetch_articles_by_ids(article_ids)
#     print("Fetched articles:", articles)
    
#     # בונים פלט עם תוכן בלבד
#     output_text = ""
#     for article in articles:
#         content = getattr(article, "content", "")
#         output_text += f"{content}\n\n---\n\n"  # מפריד בין כתבות
    
#     return output_text

# # --- יצירת UI ב-Gradio ---
# with gr.Blocks() as demo:
#     with gr.Row():
#         topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="בחר נושא")
#     with gr.Row():
#         output_area = gr.Textbox(label="תוכן הכתבות", lines=20)

#     topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

# # --- הפעלת השרת על localhost ---
# if __name__ == "__main__":
#     demo.launch(server_name="127.0.0.1", server_port=7860)















# #עובד- כתבה עם תמונה ישר אחרי הכתבה אבל בלי כותרת ושעת פרסום
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
#        # title = getattr(article, "title", "No Title")  # כותרת הכתבה
#         text, image_url = article_with_images(content)
#         result.append({
#            # "title": title,
#             "text": text,
#             "image": image_url
#         })
    
#     # מחזירים רשימה ב‑Markdown או HTML
#     md_output = ""
#     for item in result:
#        # md_output += f"### {item['title']}\n\n"
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
    
#     # רשימה סופית עם תאריך, כותרת (comments), תוכן ותמונה
#     result = []
#     for article in articles:
#         comments = getattr(article, "comments", "No Title") # כותרת הכתבה
#         date = getattr(article, "date", "")                # תאריך הכתבה
#         content = getattr(article, "content", "")         # תוכן הכתבה
        
#         text, image_url = article_with_images(content)
#         result.append({
#             "comments": comments,
#             "date": date,
#             "text": text,
#             "image": image_url
#         })
    
#     # מחזירים רשימה ב‑Markdown או HTML
#     md_output = ""
#     for item in result:
#         # תאריך + כותרת בתחילת הכתבה
#         md_output += f"**{item['date']} - {item['comments']}**\n\n"
        
#         # תוכן הכתבה
#         md_output += f"{item['text']}\n\n"
        
#         # תמונה אם קיימת
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
