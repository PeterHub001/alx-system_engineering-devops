import requests

def count_words(subreddit, word_list, after=None, counts=None):
    if counts is None:
        counts = {}

    if after is None:
        # Initial API call
        url = f"https://www.reddit.com/r/{subreddit}/hot.json"
    else:
        # Subsequent API calls
        url = f"https://www.reddit.com/r/{subreddit}/hot.json?after={after}"

    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
    }

    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        data = response.json()
        articles = data["data"]["children"]

        for article in articles:
            title = article["data"]["title"].lower()
            for word in word_list:
                if word.lower() in title:
                    if word.lower() not in counts:
                        counts[word.lower()] = 0
                    counts[word.lower()] += title.count(word.lower())

        after = data["data"]["after"]
        if after is not None:
            # Make recursive call for the next page
            count_words(subreddit, word_list, after, counts)
        else:
            sorted_counts = sorted(counts.items(), key=lambda x: (-x[1], x[0]))
            for word, count in sorted_counts:
                print(f"{word}: {count}")

