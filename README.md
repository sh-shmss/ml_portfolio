# ml_portfolio
Started out as a self-learning project, the present portfolio is an attempt to employ and expand my understanding of topics in machine learning, data science and related programming skills.

The data visualization tool visualizes word association using a network graph. It leverages the interactive features that Bokeh library offers for visualization. It finds the top n associated words with given input using NLTK and Gensim word2vec embeddings. The darker the edge the stronger the bound between the word nodes.

The language detection tool incorporates scikit-learn to detect the language of the given text. Using TF-IDF vectorization, the classifier is able to predict texts in English, German, French, Spanish, Italian, Russian, Japanese, Dutch, Polish, Portuguese, and Arabic.

The sentiment analysis tool uses TensorFlow to extract and preprocess the data (IMDB reviews dataset) and Keras to train an RNN consisting of embedding and Gated Recurrent Unit layers. The given result indicates the probability of the given review denoting positive sentiment.

The portfolio is deployed on my Raspberry Pi (hence slow response time for TensorFlow operations in the sentiment analysis component) using Nginx as the web server and uWSGI as the application server. The application itself is developed in Flask. I'm using Skeletons (my favorite, minimalist CSS framework) to style the portfolio.

I'm planning to add more interesting components with time. Please feel free to reach out and make suggestions to improve my work. I'd appreciate your feedback.
