# LBRYseed
---

[Brendon Brewer](https://open.lbry.com/@BrendonBrewer:3?r=FkXuBKiec1TjrEKg6zLLWoD2Gq1pYpgk) wrote a [Python code](https://cutt.ly/hhljDbJ) which you can use to download all content from a LBRY channel. You might want to do this for seeding your favorite channels or friends. 

<iframe id="lbry-iframe" width="560" height="315" src="https://lbry.tv/$/embed/py/a54d6156dd86b87271cd952be7c05a63ac814149?r=CJ7qFSjiY3ERc9Gj5pRPR3iqey7DdF74" allowfullscreen></iframe>

[Check Brendon's original code](https://cutt.ly/rhljKKL)

I modified so I only downloads only the blobs of the file so it doesn't takes much space from your computer (thanks to @eukrein that rescue me from non-sense complex solutions to a simple boolean switch tip) and then made executable for the Windows user :) I also added a call to ```lbrynet.exe``` to make sure its running while the script is working.  Let the seed season begin!

>OBS.: The best way to use it is to run the original Brendon's script, **that works in any O.S. with python**, this version is for windows users that doesn't know how to run python scripts :) 
>The seeding only works if you have lbrynet on or your Lbry desktop App on

Also thanks @madiator for the introduction in pyinstaller

## What does it do ? 

You can download the most recent [blobs](https://lbry.com/faq/host-content),   from your favorite channels and help to **seed** then over LBRY network.
Just type a channels name and wait for blobs download. Don't worry about space blobfile are 2Mb , Lets SEED each other and improve the user experience for everyone! You can also choose a number of posts to download or you can download the entire chosen channel !!

### How to Download and run it.

As you can see in the video below you have to reach Brendon's head in ```\dist``` folder  

<iframe id="lbry-iframe" width="560" height="315" src="https://lbry.tv/$/embed/lbryseed/26416a58726756d989b07d9eb711720cecf6ccbc?r=CJ7qFSjiY3ERc9Gj5pRPR3iqey7DdF74" allowfullscreen></iframe>

Download windows version .exe below:
[![Download](https://i.ibb.co/RYxvyf3/windows-button-download-1.png)](https://github.com/VladHZC/LBRYseeds)


### If you think its necessary a Mac OS or Linux Version comment below, but its really recommended that you learn how to run python script and its really cool to interact with lbrynet through the API 

The code : 

```
import requests
import sys
import time
import os

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
```

To transform into a .exe file I used 

```
pyinstaller --noconfirm --onedir --console --icon "C:\Users\User\Programs\LBRYchanneldownloader\a.ico" --name "LbrySeed" --add-data "C:\Users\User\Programs\LBRYchanneldownloader\lbrynet.exe;."  "C:\Users\leo13\Dropbox\Programs\LBRYchanneldownloader\c.py"
```

# Check other LBRY tools

- [LBC Today](https://cutt.ly/Dhlkfes) -> LBC price feed Extension
-  [Lbrynomics](https://cutt.ly/Bhlkf9e) ->LBRYnomics is the home of LBRY statistics where you can find all the best data for the top channels on LBRY. LBRYnomics is critical for helping you grow your channel or if you're just interested in how well other content creators are doing.
- [TurboShareKit](https://github.com/apenasrr/lbry_turbosharekit) -> Mass uploader and re-encoder for LBRY
- [LbryUP](https://github.com/VladHZC/LBRYUP) ->  Download from the internet upload on LBRY tool. 
- [Lbrylytics](https://www.lbrylytics.com/) -> LBRYlytics aims to be the first fully equipped analytics tool for LBRY content creators.


**Comment below which name you guys prefer for this new tool !!***
