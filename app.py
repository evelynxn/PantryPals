from flask import Flask, request, render_template, Response, stream_with_context
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load environment variables
load_dotenv()

# Configure Gemini
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

# Initialize the model
model = genai.GenerativeModel(
    model_name="gemini-1.5-pro-latest",
    system_instruction="You are an amazing chef who can make a recipe out of any ingredients. "
                       "Be kind, creative, and clear when giving recipes and instructions."
)

app = Flask(__name__)


@app.route("/generate", methods=["POST"])
def generate():
    ingredients = request.form.get("ingredients")
    prompt = f"Create a recipe using these ingredients: {ingredients}. Include a title, ingredients list, and clear step-by-step instructions.you are only allowed to use the ingredients given"

    def generate_stream():
        yield "<h2>🍽️ Your Recipe:</h2><ul>"  # Start an unordered list
        response = model.generate_content(prompt, stream=True)
        for chunk in response:
            if chunk.text:  # Ensure the chunk has text
                # Convert Markdown-like syntax to HTML
                formatted_text = (
                    chunk.text
                    .replace("**", "<b>")  # Remove bold markers
                    .replace("##", "<h2>")  # Replace heading markers
                    .replace("\n", "<br>")  # Replace newlines with <br>
                    .replace("* ", "<li>")  # Replace list markers with <li>
                )
                # Close tags for bold and headings
                formatted_text = formatted_text.replace("<b>", "</b>", 1).replace("<h2>", "</h2>", 1)
                yield formatted_text
        yield "</ul></pre>"  # Close the unordered list

    return Response(stream_with_context(generate_stream()), mimetype='text/html')

@app.route("/", methods=["GET"])
def home():
    return render_template("about.html")

@app.route("/chat")
def chat():
    return render_template("index.html")

@app.route("/recipeBook")
def recipe_book():
    return render_template("recipeBook.html")

@app.route("/recommendations")
def recommendations():
    return render_template("recommendations.html")

@app.route("/support")
def support():
    return render_template("support.html")



if __name__ == "__main__":
    print("Visit http://127.0.0.1:5000 in your browser ✨")
    app.run(debug=True)
