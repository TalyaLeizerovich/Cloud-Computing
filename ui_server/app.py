# import gradio as gr
# from backend import consume_article_ids, fetch_articles_by_ids, format_articles
# from config import TOPICS

# # --- פונקציית טיפול בבחירת נושא ---
# def on_topic_change(topic):
#     topic_name = TOPICS[topic]
#     # מקבלים IDs מ-Kafka
#     article_ids = consume_article_ids(topic_name)
#     print(article_ids)
#     # שולפים כתבות מה-DB לפי IDs
#     articles = fetch_articles_by_ids(article_ids)
#   #  print(articles)
#     # מחזירים לפורמט Markdown ל-Gradio
#     return format_articles(articles)

# # --- יצירת UI ב-Gradio ---
# with gr.Blocks() as demo:
#     with gr.Row():
#         topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="בחר נושא")
#     with gr.Row():
#         output_area = gr.Markdown()

#     # האירוע חייב להיות בתוך ה-Blocks
#     topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

# # --- הפעלת השרת על localhost ---
# if __name__ == "__main__":
#     demo.launch(server_name="127.0.0.1", server_port=7860)


















#עובד- כתבה עם תמונה ישר אחרי הכתבה אבל בלי כותרת ושעת פרסום
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







#כותרת עם תאריך ותמונה לצד הכתבה
import gradio as gr
from backend import consume_article_ids, fetch_articles_by_ids
from config import TOPICS
from image import article_with_images

# --- פונקציית טיפול בבחירת נושא ---
def on_topic_change(topic):
    topic_name = TOPICS[topic]

    # מקבלים IDs מ-Kafka
    article_ids = consume_article_ids(topic_name)
    print("Article IDs:", article_ids)

    # שולפים כתבות מה-DB לפי IDs
    articles = fetch_articles_by_ids(article_ids)

    # רשימה סופית עם כותרת + תאריך + טקסט + תמונה
    result = []
    for article in articles:
        # שימוש ב-getattr כדי לתמוך ב-pyodbc.Row
        content = getattr(article, "content", "")
        title = getattr(article, "comments", "No Title")   # ✅ הכותרת נשמרת ב-comments
        published_at = getattr(article, "date", "Unknown Date")  # ✅ תאריך פרסום
        text, image_url = article_with_images(content)

        result.append({
            "title": title,
            "date": published_at,
            "text": text,
            "image": image_url
        })

    # בונים Markdown עם מבנה Grid
    md_output = ""
    for item in result:
        md_output += f"### {item['title']}\n"
        md_output += f"**תאריך פרסום:** {item['date']}\n\n"

        if item['image']:
            # Grid עם שני טורים – טקסט משמאל, תמונה מימין
            md_output += "<div style='display: grid; grid-template-columns: 2fr 1fr; gap: 20px; align-items: start;'>\n"
            md_output += f"<div>{item['text']}</div>\n"
            md_output += f"<div><img src='{item['image']}' style='max-width:100%; border-radius:10px;'></div>\n"
            md_output += "</div>\n\n"
        else:
            md_output += f"{item['text']}\n\n"

    return md_output


# --- יצירת UI ב-Gradio ---
with gr.Blocks() as demo:
    with gr.Row():
        topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="בחר נושא")
    with gr.Row():
        output_area = gr.HTML()   # ✅ צריך HTML כדי שהגריד יעבוד

    topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

# --- הפעלת השרת על localhost ---
if __name__ == "__main__":
    demo.launch(server_name="127.0.0.1", server_port=7860)
