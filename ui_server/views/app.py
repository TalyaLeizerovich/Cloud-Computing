# # Works - article title, date, and content with image
# import gradio as gr
# from ui_server.controllers.backend import consume_article_ids, fetch_articles_by_ids, format_articles
# from ui_server.models.config import TOPICS

# # --- Function to handle topic selection ---
# def on_topic_change(topic):
#     topic_name = TOPICS[topic]  # Get the human-readable topic name from the config
#     # Fetch article IDs from Kafka
#     article_ids = consume_article_ids(topic_name)
#     print(article_ids)  # Print the list of article IDs for debugging
#     # Fetch articles from the database using the retrieved IDs
#     articles = fetch_articles_by_ids(article_ids)
#     # Format articles in Markdown for Gradio display
#     return format_articles(articles)

# # --- Create Gradio UI ---
# with gr.Blocks() as demo:
#     with gr.Row():
#         topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="Choose Topic")  # Dropdown for topic selection
#     with gr.Row():
#         output_area = gr.Markdown()  # Area to display formatted articles

#     # Event must be inside the Blocks context
#     topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

# # --- Launch the server on localhost ---
# if __name__ == "__main__":
#     demo.launch(server_name="127.0.0.1", server_port=8500)




# # Works - article title, date, and content with image
# import gradio as gr
# from ui_server.controllers.backend import consume_article_ids, fetch_articles_by_ids, format_articles
# from ui_server.models.config import TOPICS

# # --- Function to handle topic selection ---
# def on_topic_change(topic):
#     topic_name = TOPICS[topic]  # Get the human-readable topic name from the config
#     # Fetch article IDs from Kafka
#     article_ids = consume_article_ids(topic_name)
#     print(article_ids)  # Print the list of article IDs for debugging
#     # Fetch articles from the database using the retrieved IDs
#     articles = fetch_articles_by_ids(article_ids)
#     # Format articles in Markdown for Gradio display
#     return format_articles(articles)

# # --- Create Gradio UI ---
# with gr.Blocks(title="NextNews") as demo:  # <--- כאן הוספתי את הכותרת
#     with gr.Row():
#         topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="Choose Topic")  # Dropdown for topic selection
#     with gr.Row():
#         output_area = gr.Markdown()  # Area to display formatted articles

#     # Event must be inside the Blocks context
#     topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

# # --- Launch the server on localhost ---
# if __name__ == "__main__":
#     demo.launch(server_name="127.0.0.1", server_port=8500)




# # Works - article title, date, and content with image
# import gradio as gr
# from ui_server.controllers.backend import consume_article_ids, fetch_articles_by_ids, format_articles
# from ui_server.models.config import TOPICS

# # --- Function to handle topic selection ---
# def on_topic_change(topic):
#     topic_name = TOPICS[topic]  # Get the human-readable topic name from the config
#     # Fetch article IDs from Kafka
#     article_ids = consume_article_ids(topic_name)
#     print(article_ids)  # Print the list of article IDs for debugging
#     # Fetch articles from the database using the retrieved IDs
#     articles = fetch_articles_by_ids(article_ids)
#     # Format articles in Markdown for Gradio display
#     return format_articles(articles)

# # --- Create Gradio UI ---
# with gr.Blocks(title="NextNews") as demo:  # <--- Tab title
#     with gr.Row():
#         topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="Choose Topic")  # Dropdown for topic selection
#     with gr.Row():
#         output_area = gr.Markdown()  # Area to display formatted articles

#     # Event must be inside the Blocks context
#     topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

# # --- Launch the server on localhost ---
# if __name__ == "__main__":
#     demo.launch(
#         server_name="127.0.0.1",
#         server_port=8500,
#         favicon_path="ui_server\icons\icon.png"  # Path to your custom icon
       
#     )



import os
import gradio as gr
from ui_server.controllers.backend import consume_article_ids, fetch_articles_by_ids, format_articles
from ui_server.models.config import TOPICS

def on_topic_change(topic):
    topic_name = TOPICS[topic]
    article_ids = consume_article_ids(topic_name)
    print(article_ids)
    articles = fetch_articles_by_ids(article_ids)
    return format_articles(articles)

with gr.Blocks(title="NextNews") as demo:
    with gr.Row():
        topic_dropdown = gr.Dropdown(list(TOPICS.keys()), label="Choose Topic")
    with gr.Row():
        output_area = gr.Markdown()

    topic_dropdown.change(on_topic_change, inputs=topic_dropdown, outputs=output_area)

if __name__ == "__main__":
    # Build absolute path to icon
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    icon_path = os.path.join(base_dir, "icons", "icon.png")
    

    demo.launch(
        server_name="127.0.0.1",
        server_port=8001,
        favicon_path=icon_path
    )