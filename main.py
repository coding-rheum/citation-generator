"""
Writing citations for research papers is time-consuming! Luckily, Python can
access NCBI's database when we want to retrieve article information and help
create a citation in MLA format for the first five articles found.

Run the script in terminal:
$ python main.py

And then enter search terms to find the article you are looking for.
Enjoy!

"""


def pubmed_search(s):

    # import dependencies
    import requests
    import time

    # declare api key --> this allows to make more than 3 citation requests per second
    api_key = "d221d81fb4903f92f8dc985e1c478ad56b08"

    # this is the base url of NCBI's Entrez API
    base_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/"

    # accessing NCBI database
    database = "pubmed"

    # build query url that is used to retrieve search results
    query_url = (
            base_url + "esearch.fcgi?db=" + database + "&term=" + s + "&retmode=json&sort=relevance&api_key=" + api_key
    )

    # request in response for the search information in JSON format
    # Add a delay of 0.5 seconds between requests
    time.sleep(0.5)
    response = requests.get(query_url).json()

    # idList itself is a list, create a string with the same name
    idList = response["esearchresult"]["idlist"]

    # set condition if no articles are found
    if len(idList) == 0:
        print("No articles found! Please try another search term.")

    # condition when article(s) are found
    else:
        # for loop to iterate the first five articles in idList
        for article in idList[0:5]:

            # count articles
            total = len(idList[0:5])

            # find the index of each article
            i = idList.index(article)

            # message to show the article search
            if i == 0:
                print("------------------------")
                print("Beginning article search")
                print("------------------------")

            # create article count. python index starts at 0 so we need to add 1
            article_count = int(i) + 1

            # count number of each article
            print(f"Retrieving articles {article_count} of {total}")

            # base url to retrieve article summary
            url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esummary.fcgi?"

            # generate endpoint url from our search to retrieve information for each article
            search_url = url + "db=" + database + "&id=" + article + "&retmode=json&api_key=" + api_key

            # request article information, formatted as json
            search_response = requests.get(search_url).json()

            # create empty list for storing multiple authors per article
            author_list = []

            # try and except loop to keep the loop running
            try:
                #print("API Response:", search_response)  # Debugging output
                #print("Debugging API Response for ID:", article)
                #print(search_response)  # Print the full response from the API

                if "result" in search_response and article in search_response["result"]:
                    pubmed_id = search_response["result"][article]["uid"]
                    title = search_response["result"][article]["title"]
                    authors = search_response["result"][article]["authors"]
                    journal = search_response["result"][article]["source"]
                    pub_date = search_response["result"][article]["pubdate"]
                    volume = search_response["result"][article]["volume"]
                    issue = search_response["result"][article]["issue"]
                    pages = search_response["result"][article]["pages"]
                    doi = search_response["result"][article]["elocationid"]

                    # Process author names
                    author_list = [i["name"] for i in authors]
                    names = ", ".join(author_list)

                    # Format title
                    corrected_title = title.replace("&lt;i&gt;", "<i>").replace("&lt;/i&gt;", "</i>")

                    # Print result
                    print(f"PubMed ID: {pubmed_id}")
                    print(
                        f"{names}. {corrected_title} {journal} {pub_date[0:4]};{volume}({issue}):{pages}. {doi}"
                    )
                    print("------------------------")
                else:
                    print(f"Warning: No result found for article ID: {article}")

            except KeyError as e:
                print(f"KeyError: {e}. Missing key in response for article ID: {article}. Full response: {search_response}")
                #print(f"KeyError: {e}. Skipping article {article}.")
            except ValueError:
                print("No information found. Skipping..")
            except Exception as e:
                print(f"Unexpected error: {e}. Full response: {search_response}")
                #print(f"Unexpected error: {e}")



# asks user for search terms
term = input("Please enter a search for PubMed articles: ").replace(" ", "+")

pubmed_search(term)
