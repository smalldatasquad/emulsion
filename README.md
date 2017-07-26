# Emulsion

## What this is

These are two Python scripts.

`google_1_simplify_queries.py` helps process, consolidate, and simplify your [Google Takeout](https://takeout.google.com/settings/takeout/custom/search) search database.

`google_2_pickout_queries.py` creates a simple interface for you to search your queries and export CSV files.

## How to use `google_1_simplify_queries.py`

1. Download your search queries from [Google Takeout](https://takeout.google.com/settings/takeout/custom/search). (This can take some time, so try to do this as soon as possible!)

2. If you open the .zip archive, there should be a folder called `Searches`. Copy this to this folder (the one that `google_1_simplify_queries.py` is in).

3. In a terminal such as Terminal (Mac) or Command Prompt (PC), navigate to this folder. For help navigating, see [this for Windows](http://www.digitalcitizen.life/command-prompt-how-use-basic-commands) or [this for OSX/Linux](https://www.digitalocean.com/community/tutorials/how-to-use-cd-pwd-and-ls-to-explore-the-file-system-on-a-linux-server).

4. Run the script with `python google_1_simplify_queries.py`.

5. (For advanced users - there are some options you can explore with `-h`.)

6. The script should consolidate all of your files in `Searches` into one file called `all_google_queries_simplified.json` and `all_google_queries_simplified.csv`.


## How to use `google_2_pickout_queries.py`

1. Make sure you've already run `google_1_simplify_queries.py`.

2. Run the script with `python google_2_pickout_queries.py`. This will process your queries and give you an interactive!! way to choose between searching your queries. 

### Searching text (basic)
 
1. Try typing `why` and pressing enter.

2. If you scroll up, you should see all of the queries that has the word `why` in it. Here's one of ours: `why is pink a girl color`. 

3. The program will also save a CSV file containing all of these queries.

4. The program will then return back to the prompt, so you can search for another word.

### Searching text (OR)
 
1. Try typing `who|what` and pressing enter.

2. If you scroll up, you should see all of the queries that has the word `who` **OR** `what` in it. That is, if it matches **any** of those two words, it will give you a result. Here's one of ours: `what happens when a cow isn't milked`. 

### Searching text (AND)
 
1. Try typing `how+to` and pressing enter.

2. If you scroll up, you should see all of the queries that has the word `how` **AND** `what` in it. That is, if it matches **both** of those two words, it will give you a result. Here's one of ours: `how to eat tamarind`. 

3. The more specific your searches are, it's possible you may have zero results. For example, `rollercoaster+sleep` may return 0 results.

### Searching 'Frames' with code (intermediate)

1. At the prompt, try typing a number, like `0`, for `midnight_search`.

2. It will give you a list of all of the queries between 12am and 1am local time.

3. (This gets a little tricky if you've been in different time zones. If your computer is on NYC time, for example, but all the queries that were between 12am and 1am in NYC time. So if you were in Korea at 1:30pm, or 12:30am NYC time, then these searches would still come up.)

4. How does this work? Well, if you open `google_2_pickout_queries.py` with a text editor, and look at the code, you'll see the code annotated with comments. Even if you're completely new to Python and coding, we've written it so that you can get started changing some numbers and seeing what happens.

5. Try copying and adding some of the frames to make some new types of 'Frames'.


### Making your own filters/frames (advanced)

If you're totally comfy with Python, then you probably know what you're doing. Some notes/explanations:

- All 'Frames' are functions stored in an OrderedDict called `frames`, so that user input automatically grabs all of the available functions and makes them available for selection. 

- Each frame is a function passed to Python's `filter`, so only needs true/false returns.

- Everything is Unicode-friendly.

#### Some ideas we had:

- Weather api: Who am I when it was rainy, and what did I search for?
- Temperature api: Who am I when it was cold, and what did I search for?
- Astrology frame: who was I when Mercury was in retrograde?
- Music: What are all the music lyrics I searched for?
- Pattern recognition: are there repeated searches over time?
- Clustering: Is it possible to use vector representations of sentences and do some sort of dimensionality reduction (T-SNE) or clustering (K-means?) to see what major clusters of 'search terms' are? Could these be a way to identify "How many Cindy-Sherman-esque identities do I have?"


