import re
from collections import defaultdict
import streamlit as st

# Sample e-commerce reviews for shirts
ecommerce_reviews = [
    "The shirt fits perfectly, the size is exactly as described.",
    "I didn't like the shirt color, it was much lighter than shown in the picture.",
    "Amazing quality for the price, the material feels premium.",
    "The shirt was too small, had to return it. Disappointed.",
    "Loved the color and quality of the shirt. Will buy again!",
    "The size is perfect, and the fabric feels great on the skin.",
    "The shirt color was dull, not as vibrant as I expected.",
    "The shirt quality is terrible, it shrunk after one wash.",
    "Very comfortable shirt, fits true to size and the color is nice.",
    "The shirt was poor quality, threads were coming loose.",
    "The delivery was fast, and the product arrived on time.",
    "Shipping took too long, I wasn't happy with the delay.",
    "The delivery was on time and the packaging was great.",
    "Comparing this with other brands, the quality is much better.",
    "The shipping was delayed but the product is worth it."
]

# Function to clean and preprocess reviews
def clean_reviews(reviews):
    cleaned_reviews = []
    for review in reviews:
        # Remove special characters and digits
        review = re.sub(r'\W+', ' ', review)
        # Lowercase all words
        review = review.lower()
        cleaned_reviews.append(review)
    return cleaned_reviews

# Define logic to classify reviews into categories and sentiments
def classify_review(review):
    review = review.lower()

    # Check for size-related keywords
    if any(word in review for word in ['size', 'fit', 'small', 'large']):
        topic = "Size"

    # Check for color-related keywords
    elif any(word in review for word in ['color', 'vibrant', 'dull', 'light']):
        topic = "Color"

    # Check for quality-related keywords
    elif any(word in review for word in ['quality', 'material', 'fabric', 'premium']):
        topic = "Quality"
    
    # Check for delivery-related keywords
    elif any(word in review for word in ['delivery', 'shipping', 'arrived', 'delayed']):
        topic = "Delivery & Shipping"
    
    # Check for on-time delivery-related keywords
    elif any(word in review for word in ['on time', 'ontime', 'fast', 'timely']):
        topic = "On-time Delivery"

    # Check for comparison-related keywords
    elif any(word in review for word in ['compare', 'comparison', 'better', 'worse']):
        topic = "Comparison"
    
    else:
        topic = "Other"

    # Classify sentiment as positive or negative
    positive_keywords = ['perfect', 'loved', 'amazing', 'comfortable', 'great', 'nice', 'buy again', 'better', 'on time', 'fast', 'worth']
    negative_keywords = ['poor', 'terrible', 'disappointed', 'shrunk', 'dull', 'loose', 'return', 'delayed', 'worse', 'too long']

    if any(word in review for word in positive_keywords):
        sentiment = "Positive"
    elif any(word in review for word in negative_keywords):
        sentiment = "Negative"
    else:
        sentiment = "Neutral"
    
    return topic, sentiment

# Initializing Streamlit app
st.title("E-Commerce Review Classifier")

# Adding a new review via input box
st.subheader("Add a New Review")
new_review = st.text_area("Enter your review here:", "")

if st.button("Classify Review"):
    if new_review:
        ecommerce_reviews.append(new_review)

# Preprocessing the existing reviews
cleaned_reviews = clean_reviews(ecommerce_reviews)

# Group reviews by their assigned topics and sentiments
grouped_reviews = defaultdict(lambda: defaultdict(list))
for i, review in enumerate(cleaned_reviews):
    topic, sentiment = classify_review(ecommerce_reviews[i])
    grouped_reviews[topic][sentiment].append(ecommerce_reviews[i])

# Layout for displaying reviews with expander sections
st.subheader("Grouped Reviews by Topic and Sentiment")

# Use expanders to keep the UI compact
for topic, sentiment_dict in grouped_reviews.items():
    with st.expander(f"Topic: {topic}", expanded=False):
        for sentiment, reviews in sentiment_dict.items():
            st.write(f"**{sentiment} Reviews:**")
            for review in reviews:
                st.write(f"- {review}")
            st.write(f"**Total {sentiment} reviews: {len(reviews)}**")  # Adding review count

# Review Summary after all the reviews
st.subheader("Review Summary")

for topic, sentiment_dict in grouped_reviews.items():
    st.write(f"### {topic}")
    total_reviews = sum(len(reviews) for reviews in sentiment_dict.values())
    st.write(f"Total Reviews: {total_reviews}")
    for sentiment, reviews in sentiment_dict.items():
        st.write(f"{sentiment}: {len(reviews)} reviews")
    st.write("---")
