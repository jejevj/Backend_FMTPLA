from fastapi import FastAPI, Query
import requests
import xmltodict
from fastapi.responses import JSONResponse
import json
import os

app = FastAPI()

FLICKR_FEED_URL = "https://www.flickr.com/services/feeds/photos_public.gne"

# A global variable to hold the author data temporarily, or you can use a database for persistent storage
author_data = []


@app.get("/flickr-feed")
async def get_flickr_feed(
    id: str = Query(None, description="A single user ID to fetch the feed for."),
    ids: str = Query(None, description="A comma delimited list of user IDs to fetch the feed for."),
    tags: str = Query(None, description="A comma delimited list of tags to filter the feed by."),
    tagmode: str = Query("all", description="Control whether items must have ALL or ANY tags (default: all)."),
    format: str = Query("atom", description="The format of the feed (default: Atom 1.0)."),
    lang: str = Query("en-us", description="The display language for the feed (default: en-us).")
):
    global author_data

    # Path to the authors JSON file
    authors_file = "authors.json"

    # Load existing author data from the file, if it exists
    if os.path.exists(authors_file):
        with open(authors_file, "r") as f:
            author_data = json.load(f)
    else:
        author_data = []

    # Construct the query parameters
    params = {
        "id": id,
        "ids": ids,
        "tags": tags,
        "tagmode": tagmode,
        "format": format,
        "lang": lang,
    }

    # Remove None values from params to only send the specified ones
    params = {key: value for key, value in params.items() if value is not None}

    try:
        # Fetch the XML feed from Flickr with the specified query parameters
        response = requests.get(FLICKR_FEED_URL, params=params)

        # Check if the request was successful
        if response.status_code != 200:
            return JSONResponse(status_code=response.status_code, content={"error": "Failed to fetch the feed"})

        # Parse the XML data
        xml_data = response.content
        parsed_data = xmltodict.parse(xml_data)

        # Extract necessary data from the parsed XML
        feed_title = parsed_data["feed"]["title"]
        entries = parsed_data["feed"].get("entry", [])

        # Format only necessary data into a simplified JSON structure
        formatted_data = {
            "feed_title": feed_title,
            "photos": []
        }

        # Ensure entries are always treated as a list
        if isinstance(entries, dict):
            entries = [entries]

        for entry in entries:
            # Handle case where link might be a dict instead of a list
            links = entry.get("link", [])
            if isinstance(links, dict):
                links = [links]  # Convert single dict to list for uniformity

            # Handle case where categories might be a dict instead of a list
            categories = entry.get("category", [])
            if isinstance(categories, dict):
                categories = [categories]

            # Extracting specific required fields
            photo_data = {
                "title": entry.get("title"),
                "photo_link": links[0]["@href"] if len(links) > 0 else None,  # Link to the photo page
                "image_url": links[1]["@href"] if len(links) > 1 else None,   # Direct image URL (from the enclosure link)
                "published": entry.get("published"),
                "updated": entry.get("updated"),
                "date_taken": entry.get("flickr:date_taken"),
                "author": entry["author"].get("name"),
                "author_url": entry["author"].get("uri"),
                "author_nsid": entry["author"].get("flickr:nsid"),  # Extracting nsid
                "author_buddyicon": entry["author"].get("flickr:buddyicon"),  # Extracting buddyicon URL
                "tags": [category["@term"] for category in categories]  # Extracting all tags
            }
            formatted_data["photos"].append(photo_data)

            # Collect author data to save later
            author_entry = {
                "author": photo_data["author"],
                "author_url": photo_data["author_url"],
                "author_nsid": photo_data["author_nsid"],
                "author_buddyicon": photo_data["author_buddyicon"]
            }

            # Check if the author already exists in the author_data list
            if not any(author['author_nsid'] == author_entry['author_nsid'] for author in author_data):
                # Add new author to the author_data list if not already present
                author_data.append(author_entry)

        # Save the updated author data to a JSON file
        with open(authors_file, "w") as f:
            json.dump(author_data, f, indent=4)

        # Return the formatted data as a JSON response
        return JSONResponse(content=formatted_data)
    
    except Exception as e:
        return JSONResponse(status_code=500, content={"error": str(e)})

@app.get("/authors", response_class=JSONResponse)
async def fetch_authors():
    authors_file = "authors.json"

    # Check if the file exists
    if os.path.exists(authors_file):
        try:
            # Open and read the authors.json file
            with open(authors_file, "r") as f:
                author_data = json.load(f)
            return JSONResponse(content=author_data)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": f"Error reading authors file: {str(e)}"})
    else:
        return JSONResponse(status_code=404, content={"error": "Authors file not found"})
    
from difflib import get_close_matches

@app.get("/search-authors")
async def search_authors(query: str):
    authors_file = "authors.json"

    # Load the authors from the JSON file
    if os.path.exists(authors_file):
        try:
            with open(authors_file, "r") as f:
                author_data = json.load(f)
        except Exception as e:
            return JSONResponse(status_code=500, content={"error": f"Error reading authors file: {str(e)}"})
    else:
        return JSONResponse(status_code=404, content={"error": "Authors file not found"})

    # Normalize the query to be case-insensitive
    query = query.lower()

    # Find exact and partial matches
    exact_matches = []
    partial_matches = []

    # Iterate through authors to check for matches
    for author in author_data:
        author_name = author['author'].lower()

        # Exact match
        if author_name == query:
            exact_matches.append(author)
        # Partial match (check if the query is part of the author's name)
        elif query in author_name:
            partial_matches.append(author)

    # Also, get the closest matches using difflib for similarity matching (optional)
    all_author_names = [author['author'] for author in author_data]
    similar_matches = get_close_matches(query, all_author_names, n=5, cutoff=0.6)

    # Find author objects for similar matches
    similar_author_matches = [author for author in author_data if author['author'] in similar_matches]

    # Combine the results
    search_results = {
        "exact_matches": exact_matches,
        "partial_matches": partial_matches,
        "similar_matches": similar_author_matches
    }

    # Return the search results
    return JSONResponse(content=search_results)

