#!/usr/bin/env python

import requests
import sys
import time
import os
import sys

toolbar_width = 100

# setup toolbar
sys.stdout.write("[%s]" % ("" * toolbar_width))
sys.stdout.write("               Wait Lbrynet Startup, Thanks Brendon")
sys.stdout.write("\b" * (toolbar_width+1)) # return to start of line, after '['


os.system("start cmd /c lbrynet start")
# LBRY JSON RPC

while True:
    for i in range(toolbar_width):
        time.sleep(0.1) 
        sys.stdout.write("-")
        sys.stdout.flush()

    sys.stdout.write("]\n")

    HOST = "http://localhost:5279"

    # Wait time (seconds)
    WAIT = 20.0

    def get_claim_id(url):
        """
        Input: url
        Output: Claim ID of the resolved claim.
        """
        print("Resolving channel...", end="", flush=True)
        response = requests.post(HOST,
                                 json={"method": "resolve",
                                       "params": {"urls": [url]}}).json()
        claim = [response["result"][key] for key in response["result"]][0]
        try:
         
            claim_id = claim["claim_id"]
        except:
            print("channel not found. Exiting.")
            sys.exit(-1)
        print(f"done.\nThe claim_id is {claim_id}.", flush=True)
        return claim_id
        


    def get_streams(claim_id, limit=None):
        print("Searching for publications...", end="", flush=True)
        response = requests.post(HOST,
                                 json={"method": "claim_search",
                                       "params": {"channel_ids": [claim_id]}}).json()
        num = response["result"]["total_items"]
        pages = response["result"]["total_pages"]
        print(f"There are {num} files in this channel.", flush=True)

        # Loop over page, get canonical urls of the streams, and sd hashes
        urls = []
        sd_hashes = []
        for page in range(1, pages+1):
            print(f"\rProcessing page {page}/{pages}.", flush=True, end="")
            response = requests.post(HOST,
                                     json={"method": "claim_search",
                                           "params": {"page": page,
                                                      "channel_ids": [claim_id],
                                                      "order_by": "release_time"}}).json()
            urls += [item["canonical_url"] for item in response["result"]["items"]\
                        if item["value_type"] == "stream"]
            sd_hashes += [item["value"]["source"]["sd_hash"]\
                                for item in response["result"]["items"]\
                                if item["value_type"] == "stream"]
            if limit is not None and len(urls) >= limit:
                urls = urls[0:limit]
                sd_hashes = sd_hashes[0:limit]
                break

        print("")

        return [urls, sd_hashes]


    def have_all_blobs(sd_hash):
        """
        See whether you already have all blobs.
        """
        response = requests.post(HOST,
                                 json={"method": "file_list",
                                       "params": {"sd_hash": sd_hash}}).json()
        items = response["result"]["items"]
        if len(items) == 0:
            return False
        else:
            return items[0]["blobs_remaining"] == 0


    if __name__ == "__main__":
        channel = input("Enter the LBRY URL of the channel: ")
        global claim_id
        claim_id = get_claim_id(channel)

        print("""Enter maximum number of files to download, and it'll get the most recent ones.
    Or, just hit enter to download the entire channel (not recommended unless you're brave and knowledgeable!).
    If you've never used this before, try a low number like 3 or 5:""", end=" ")
        limit = input("")
        if len(limit) == 0:
            limit = None
        else:
            limit = int(limit)

        urls, sd_hashes = get_streams(claim_id, limit)

        for i in range(len(urls)):
            url = urls[i]
            sd_hash = sd_hashes[i]
            print("--------------------------------------------------------------")
            print(url)
            print("--------------------------------------------------------------")
            if have_all_blobs(sd_hash):
                print("Already have all blobs for this file.", flush=True)
            else:
                print(f"lbrynet get {url}.", flush=True)
                requests.post(HOST, json={"method": "get",
                                          "params": {"uri": url,"save_file":False}}).json()
                if i < len(urls)-1:
                    print(f"Waiting {WAIT} seconds, to avoid problems with too \nmany downloads at one time.", flush=True)
                    time.sleep(WAIT)

            print("\n\n")

        print("Thanks for seeding LBRY content. After waiting a while,\nyou should run this again to make sure all downloads finished.\nYou may need to do this several times.")



