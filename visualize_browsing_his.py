import pandas as pd
from urllib.parse import urlparse
import matplotlib.pyplot as plt
import datetime

def extract_domain(url):
    parsed_url = urlparse(url)
    return parsed_url.netloc

if __name__ == "__main__":
    js = pd.read_json("BrowserHistory.json")
    ls = js["Browser History"].to_list()
    df = pd.json_normalize(ls)
    
    # compute the first and last dates to record the browsing history
    start_date = datetime.datetime.fromtimestamp(min(df["time_usec"]) / 10**6)
    end_date = datetime.datetime.fromtimestamp(max(df["time_usec"]) / 10**6)
    start_date_formatted = start_date.strftime("%Y %B")
    end_date_formatted = end_date.strftime("%Y %B")
    
    # simply the url to domain names
    df['domain'] = df['url'].apply(extract_domain)
    
    # compute the top 10 visited websites
    result = df.groupby("domain")["url"].agg(["count"])
    sorted_result = result.sort_values("count", ascending=False)
    sorted_result_top_50 = sorted_result.iloc[:50]
    
    # create the figure and save it
    fig = plt.figure(figsize=(20, 10))
    ax = plt.subplot(1, 1, 1)
    ax.barh(sorted_result_top_50.index, sorted_result_top_50["count"])
    plt.xticks(rotation=90, fontsize=10)
    ax.invert_yaxis()
    plt.title(f"Number of website accesses from {start_date_formatted} to {end_date_formatted}")
    plt.xlabel("Number of access")
    # plt.show()
    plt.savefig("browsing_history.png")

