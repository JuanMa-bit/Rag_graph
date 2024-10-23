NODE_FILTER_PROMPT  = """
Objective:

The goal is given a question and a set of entities, ranks the entities based on their importance to answer the question and returns the top 
𝑘
k entities in descending order of importance.

Instructions:

Input Parameters:

question (str): The question for which the entities need to be ranked.
entities (list of str): A list of entities that may be relevant to answering the question.
k (int): The number of top entities to return based on their importance.
Output:

A tuple of the top 
𝑘
k entities ordered from most important to least important.
Steps to Achieve the Objective:

Step 1: Preprocessing the Inputs:
Tokenize and preprocess the question to remove stopwords, punctuation, and to standardize the text (e.g., lowercasing).
Tokenize and preprocess each entity similarly.
Step 2: Entity Relevance Scoring:
Calculate the relevance score for each entity in relation to the question. 
Step 3: Ranking the Entities:
Rank the entities based on their relevance scores.
Select the top 
𝑘
k entities with the highest scores.
Step 4: Returning the Results:
Return the top 
𝑘
k entities as a tuple in descending order of importance.
EXAMPLE 1:

Question: "What are the symptoms of diabetes?"
Entities: ["Insulin", "Blood Sugar", "Thirst", "Fatigue", "Weight Loss", "Pancreas", "Diet"]
Top 
𝑘
k: 3
RESPONSE: ("Thirst", "Fatigue", "Weight Loss")
END OF EXAMPLE 1

EXAMPLE 2:

Question: "Which planets are known as the gas giants?"
Entities: ["Earth", "Jupiter", "Mars", "Saturn", "Venus", "Uranus", "Neptune"]
Top 
𝑘
k: 2
RESPONSE: ("Jupiter", "Saturn")
END OF EXAMPLE 2
======================================================================

======================================================================
REAL DATA: The following section is the real data. You should use only this real data to prepare your answer. Generate Entity Types only.
question: {question}
entities: {entities}
k:{k}
RESPONSE:
{{<k entities>}}
"""
RELATION_FILTER_PROMT = """
You are an assistant that specializes in information extraction and ranking. Given a list of relationships and a question, your task is to identify and rank the most important relationships based on their relevance for answering the question. Return the top k relationships in order of importance.

Input:
- Text: "{text}"
- Relationships: {relationships}
- Top k: {k}

Instructions:
1. Analyze the provided text to understand its key themes, entities, and overall context.
2. Evaluate each relationship from the list based on how relevant and significant it is to the main points of the text.
3. Rank the relationships from the most important to the least important according to their relevance to the text.
4. Return the top k relationships in descending order of importance.

Output format:
[
    "1: relationship_1",
    "2: relationship_2",
    ...
    "k: relationship_k"
]

Example:

Input:
- Text: "The rapid advancements in artificial intelligence have significantly impacted various industries, including healthcare, finance, and transportation."
- Relationships: ["AI and healthcare", "AI and finance", "AI and transportation", "AI and entertainment"]
- Top k: 3

Output:
[
    "1. AI and healthcare",
    "2. AI and finance",
    "3. AI and transportation"
]

Text: "{text}"
Relationships: {relationships}
Top k: {k}

"""