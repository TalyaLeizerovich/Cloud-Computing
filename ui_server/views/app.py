import os
import gradio as gr
from ui_server.controllers.backend import consume_article_ids, fetch_articles_by_ids, format_articles

TOPICS = ["sports", "politics", "entertainment", "technology", "others"]

def on_topic_click(topic):
    try:
        article_ids = consume_article_ids(topic)
        articles = fetch_articles_by_ids(article_ids)
        result = format_articles(articles)
        return result
    except Exception as e:
        return f" Error while retrieving articles for topic {topic}: {e}"

with gr.Blocks(
    title="NextNews",
    theme=gr.themes.Soft(),
    css="""
/*  Style for topic buttons */
.topic-btn {
    background-color: #ff4d4d !important;
    color: white !important;
    border: none !important;
    border-radius: 10px !important;
    font-weight: bold !important;
    padding: 10px 18px !important;
    transition: background-color 0.3s ease !important;
}
.topic-btn:hover {
    background-color: #ff6666 !important;
}

/*  Set all text content to black */
.markdown-body, .gr-markdown, p, h1, h2, h3, h4, h5, h6, li, span {
    color: black !important;
}

/*  News card layout and styling */
.news-card {
    display: flex;
    flex-direction: row-reverse; /* Image on the right */
    align-items: flex-start;
    background-color: #fafafa;
    border: 1px solid #ddd;
    border-radius: 12px;
    padding: 15px;
    margin: 20px 0;
    box-shadow: 0 2px 5px rgba(0,0,0,0.1);
    transition: transform 0.2s ease, box-shadow 0.2s ease;
}
.news-card:hover {
    transform: scale(1.01);
    box-shadow: 0 4px 10px rgba(0,0,0,0.15);
}
.news-image img {
    width: 300px;
    height: 230px;
    object-fit: cover;
    border-radius: 10px;
    margin-left: 20px;
}
.news-content {
    flex: 1;
}
.news-content h3 {
    margin: 0;
    font-size: 20px;
    color: #222;
}
.news-content .date {
    font-size: 14px;
    color: #777;
    margin-bottom: 8px;
}
.news-content .text {
    font-size: 16px;
    line-height: 1.5;
    color: #000;
}
"""
) as demo:
    #  Main title centered at the top
    gr.HTML("<h1 style='text-align:center; color:black; font-weight:bold; font-family:Arial;'>NextNews</h1>")

    #  Topic buttons row
    with gr.Row():
        buttons = []
        for topic in TOPICS:
            btn = gr.Button(topic.capitalize(), elem_classes="topic-btn")
            buttons.append(btn)

    #  Use HTML instead of Markdown to preserve custom layout
    output_area = gr.HTML("")

    #  Link each button to the function displaying articles
    for btn, topic in zip(buttons, TOPICS):
        btn.click(fn=on_topic_click, inputs=gr.Textbox(value=topic, visible=False), outputs=output_area)

if __name__ == "__main__":
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_dir, "icons", "icon.png")

    #  Launch the Gradio app
    demo.launch(
        server_name="127.0.0.1",
        server_port=8001,
        favicon_path=icon_path
    )
