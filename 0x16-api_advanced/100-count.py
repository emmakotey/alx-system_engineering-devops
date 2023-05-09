#!/usr/bin/python3
"""Contains the count_words function"""
import requests

def count_words(subreddit, word_list, last_post=None, word_counts=None):
    """
    Recursively query the Reddit API, parse the title of all hot articles,
    and print a sorted count of given keywords.

    Args:
        subreddit (str): The name of the subreddit to search.
        word_list (list): A list of words to count occurrences of.
        last_post (str): The ID of the last post queried, used for pagination.
        word_counts (dict): A dictionary mapping words to their counts.

    Returns:
        None. Prints the sorted counts of each word.
    """
    if not word_counts:
        word_counts = {}

    url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    headers = {"User-Agent": "Mozilla/5.0"}

    params = {"limit": 100}
    if last_post:
        params["after"] = last_post

    response = requests.get(url, headers=headers, params=params)

    if response.status_code != 200:
        print(f"Error: {response.status_code}")
        return

    posts = response.json()["data"]["children"]
    for post in posts:
        title = post["data"]["title"].lower()

        # Count occurrences of each word
        for word in word_list:
            if word.lower() in title and not any(c.isalpha() for c in title[title.find(word.lower())-1: title.find(word.lower())]) and not any(c.isalpha() for c in title[title.find(word.lower())+len(word): title.find(word.lower())+len(word)+1]):
                if word.lower() not in word_counts:
                    word_counts[word.lower()] = 1
                else:
                    word_counts[word.lower()] += 1

    # If there are more posts to query, recursively call the function
    if "after" in response.json()["data"]:
        count_words(subreddit, word_list, response.json()["data"]["after"], word_counts)
    else:
        # Sort the word counts by count (descending) and then by word (ascending)
        sorted_counts = sorted(word_counts.items(), key=lambda x: (-x[1], x[0]))
        for word, count in sorted_counts:
            print(f"{word}: {count}")

