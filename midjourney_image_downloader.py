import os
import re
import requests
import urllib.request
import json
from datetime import datetime

# -------- CONFIG ------------------
# Get your user ID from the "view as visitor link (https://www.midjourney.com/app/users/.../) on your Midjourney gallery
USER_ID = "c390c8aa-e8e0-4b19-9f4e-d82f95b9caf3"
# In your browser's dev tools, find the `__Secure-next-auth.session-token` cookie.
SESSION_TOKEN = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..lIlgioRJUxuPtvLJ.exS45d1BRe45O4arMsde6x-gNkTCiiV8N_Nv5bEZqh7ob1EM5HOdJELcDRmKKc67Rp1XVeJ9dSn8DkMVaoO5cDy6SPwqc6ynByS4GMZctFwX7ZYU1b6PQ4d80MkMaOMy5i5SVbyazlPwH72M8Of3-yo7GCy9dxXkWGk9pf9vdRoAjBFqo0FqCrzaPE3Lh8Ub2xOReY35PYEkJkbloyH6hrT8Yv9U0Ph-uCr0MtJgcr25Uy8svUg2RAUUABlB8gyCkPlmwLPiI5-1qnR7-E5jYJ754Um9I4wFsvfOLGix1eyR-w0joEr9cABIsrgXExT4TTSAuoC_P-8IX1s6DNutAqU_KQe7dpBEK30wcl_-hokYH5UCg8LIZIRgv2WDYxtamKYMBeQOOyuvqAkhBUYEKPw511FfV-Lk1ugJ3b4BH9FVjlqUqhP9Q_cEMHDz995oBE1_4Y9HYKOM0TKBa0-vwsRT9Ct7xPRxNqycBzp2-1bShbdbphHCPE2qjzLhXr9CYxjaut7Io61kCeNNZ3YMaqQaVo1NxqGbUwIMROs4I3xO7-qWE_1d795HTcvC31vyqXfEO6913R3iFkDUCCvox6amyHmGO_kKaXhcpUwNME37PgUzcs5jb7Nc3528JoNnImFx1NiuYdEUKlfhIkL9z40_YkGHqDSiWLwYxh_ScMlTEI85-GYQE7tYoZxvZYU051gYewxZnbns8gm0Sa60Jnv_hwDNLzY-pWM0O7gILF3lfL_TuiVxjmSZgc9Q2x6wYvWx0h3LFgczx0IUDxp6xhTpn0PhNwDMH9m0wFGMNuOdi4IKnA8Pyi4vOr917I6-zAKkwluPh-4JZ5DPOE_t8EvRabUur0i9TVCoN9sPQVZFNXI7zxRKydcPLFKII2C0Pk-Qp4Pmee7GMaq1IwwNx87t03-tnRJGaFxgddoc5aulujpxU4D4B7MDyoitD0ttbzGp9OwwTix3Xha-Gx74uiJjsH_0RCV4xz9E39kCnQaMnG_Vuu2A2PBB13LAnJCP3EiGE7m43uFZ2-uOqH4go_abLQdflqZTCahLQ_rkrTPa-7uLvWuL_0WIUH5s_l33RWf3a3oS6CmzIJzeEW74CuEDaxqLoujVtGJDe_IUbkUkBJYz_r9Pqb7NGML_UYqBE-X8ET1GiBSHKGvvW5cx58ZEYbknZZq45VNSSSo95MPSaC8ZW7CIqMSrkbbc_E0mWgaaij8X68WDWAaLxNOtdUeXtHTuRe8CMFFVicsMgALBfiJEgPTB9bmCqKlV_7LsB32eDPikcycwOx6KGpnAdTh9z7kVBbUZ8TzQeVRK8_uT9bl7mKgVWMT28uNxwi8b6c8DuAzC8g3R8p3cWMj8JfgRe9nhfPXSTrhMY_F7qD2h4xvBroZ38oEMnw8SvNB4GBGlTe6ZZvxJzkv3gm-f3a74bH8MqyR6F5B5Ke1xAVSNjxUNKtmPc70ibdX0hDpuPEaSBYTp3GxAK_xRRcrWkgZdmIUsSBLKaIz586le6yonUWQxL_xUGPHH67qDxujrlPrz1bYfSL7HQFRBdfamBuER3QIl8pZOjcEQfySyjzu16dlG9tsQ6L3A7EvbDFRBooWisZkk7aLk5e8ewTVX07OQzUWlFv8JDvldGrMn_iMaYZnCLPa8W_rnCFNsWUH9MNWE3Du3xEUbpp2OaSmP4Nb-JVdc-vXib_8uGt6OUJpdpLhgr11LC8IMP0vcu-hIhkv7UPL5HaF-FLguWzgkKlKAK6gBg8O2GFWFNH2lH90ayQp6EBkUt1yciDkboVrPbcVUfuNVsFjb6nUXQPcP5wIKlGitUgFcIaUauwiEEaHIl-ZtqJ7dE5veub6RCLFb9yRBWf2F3urjqlQlLxEegebkczfy6se46uliqXdKKqZUdpAaqG0WO76yMNwCQql3USFFZ3WPyM9a5yfv2dINwKLx9je49Ma54--UT4j-CvNFEtJyu2uhM5iAxh41sUfUS3Ly_xJOChDnQ_BR8KlHwf8JtzWcG6Q1p8CQem5sFbk17GMKNYdhjZ8N2B-CiSKI4P1i4WMiiKKONBLio9f2I8gvONih39Chlz563-oLCHX4FITvnzfZt5Rk0K51B167lsEWIqRcmeOD-ZZt7zRI1K5zxxNhVErnVZrqPoWr94d6c7-rjuOjxBhjptXW2CZDb0UvdQ7zLmNaAEjMmuqPQy5sXaL6DpiJpMxUcD23vzJUn_jQfWgOyOM1YV2PIxKGZNKxTMqi7uFnBmtMP8eLD4GhbtPJw-wgwZ1cWZ93TLnNvZ5DCaXdIAvFttWqnWVz_z3ZRtHVgDx6uy5M5KTSuL62LKUOBGgML3oAx1jj4K8jufRi8I-XJhY38c4e-N0OptNHqg1fLbhy9L1HZ-65frp13c07MXwTLziViptV8So7awHXh104A3zNMe4wyAWbSe8XHbghtjsfkDCFaw_a7cZtOzUi6J8Xf8PMQosBk39nW0g3pIfpO4y-3TPfh-xuCZEJyjfxkr2i6JUZzO4IMmHl.-UW2_qvCkui_Rq-gnsd89Q"
# ---------------------------------

# Get the username of the current Windows PC
username = os.getlogin()
# Create the file path
filepath = f"C:\\Users\\{username}\\Downloaded_image_id.txt"
existing_ids = set()
# Check if the file exists
if not os.path.exists(filepath):
    # Create the file if it doesn't exist
    with open(filepath, 'w') as file:
        pass
else:
    with open(filepath, 'r') as file:
        existing_ids=set(line.strip() for line in file)
        # print(f"existing id::{existing_ids}")

# ------- OPTIONS -----------------
UPSCALES_ONLY = False
GRIDS_ONLY = False
USE_DATE_FOLDERS = False
GROUP_BY_MONTH = False
SKIP_LOW_RATED = False
# ---------------------------------

UA = 'Midjourney-image-downloader/0.0.1'
HEADERS = {'User-Agent': UA}
COOKIES = {'__Secure-next-auth.session-token': SESSION_TOKEN}
# ORDER_BY_OPTIONS = ["new", "oldest", "hot", "rising", "top-today", "top-week", "top-month", "top-all", "like_count"]
ORDER_BY_OPTIONS = ["hot","rising","top-all"]


def get_api_page(order_by="new", page=1):
    if(order_by == "hot"):
        api_url = "https://www.midjourney.com/api/app/recent-jobs/?amount=35"\
            "&dedupe=true&jobStatus=completed&jobType=upscale&orderBy=hot"\
                f"&page={page}&refreshApi=0&searchType=null&service=main"\
                    "&user_id_ranked_score=0%2C4%2C5&_ql=todo"\
                        "&_qurl=https%3A%2F%2Fwww.midjourney.com%2Fapp%2Ffeed%2F"
    else:
        api_url = "https://www.midjourney.com/api/app/recent-jobs/?amount=35"\
            f"&dedupe=true&jobStatus=completed&jobType=upscale&orderBy={order_by}"\
            f"&page={page}&refreshApi=0&searchType=null&service=main"\
            "&user_id_ranked_score=0%2C4%2C5&_ql=todo"\
            f"&_qurl=https%3A%2F%2Fwww.midjourney.com%2Fapp%2Ffeed%2F%3Fsort%3D{order_by}"
    
    
    # api_url = "https://www.midjourney.com/api/app/recent-jobs/?amount=35"\
    #         "&dedupe=true&jobStatus=completed&jobType=upscale&orderBy=hot"\
    #             f"&page=32&refreshApi=0&searchType=null&service=main"\
    #                 "&user_id_ranked_score=0%2C4%2C5&_ql=todo"\
    #                     "&_qurl=https%3A%2F%2Fwww.midjourney.com%2Fapp%2Ffeed%2F"

    print(f"API URL = {api_url}")
    response = requests.get(api_url, cookies=COOKIES, headers=HEADERS)
    result = response.json()
    return result


def download_page(page):
    for idx, image_json in enumerate(page):
        # print("image_json:")
        # print(image_json)
        if isinstance(image_json, dict):
            filename = save_prompt(image_json)
            if filename:
                print(f"{idx+1}/{len(page)} Downloaded {filename}")


def ensure_path_exists(year, month, day, image_id):
    if USE_DATE_FOLDERS:
        if not os.path.isdir(f"jobs/{year}"):
            os.makedirs(f"jobs/{year}")
        if not os.path.isdir(f"jobs/{year}/{month}"):
            os.makedirs(f"jobs/{year}/{month}")
        if GROUP_BY_MONTH:
            if not os.path.isdir(f"jobs/{year}/{month}/{image_id}"):
                os.makedirs(f"jobs/{year}/{month}/{image_id}")
            return f"jobs/{year}/{month}/{image_id}"
        else:
            if not os.path.isdir(f"jobs/{year}/{month}/{day}"):
                os.makedirs(f"jobs/{year}/{month}/{day}")
            if not os.path.isdir(f"jobs/{year}/{month}/{day}/{image_id}"):
                os.makedirs(f"jobs/{year}/{month}/{day}/{image_id}")
            return f"jobs/{year}/{month}/{day}/{image_id}"
    else:
        if not os.path.isdir(f"jobs"):
            os.makedirs(f"jobs")
        return f"jobs"


def downloaded_previously(id):
    
    if id in existing_ids:
        return True
    
    existing_ids.add(id)
    with open(filepath, 'a') as file:
        file.write("\n")
        file.write(str(id))
    return False
    
def should_skip(filename):
    filename = filename.replace("(","").replace(")","")
    strings_to_detect = ["cat", "dog", "squirrel", "bear", "lion", "mouse", "colouring", "coloring", "fashion", "flower", "flowers", "cats", "dogs", "squirrels", "bears", "lions", "mice"]
    words = filename.split()
    for word in words:
        if word in strings_to_detect:
            return True        
    return False

def save_prompt(image_json):
    image_paths = image_json.get("image_paths", [])
    image_id = image_json.get("id")
    prompt = image_json.get("prompt")
    enqueue_time_str = image_json.get("enqueue_time")
    enqueue_time = datetime.strptime(enqueue_time_str, "%Y-%m-%d %H:%M:%S.%f")
    year = enqueue_time.year
    month = enqueue_time.month
    day = enqueue_time.day
    if(prompt is not None):
        skip_check = prompt.replace(",", "").replace("*", "").replace("'", "").replace(":", "").replace(
            "__", "_").replace("<", "").replace(">", "").replace("/", "").replace(".", "").replace("\"","").replace(
                "\\","").replace("?","").replace("|","").lower().strip("_*")[:100]
        filename = skip_check.replace(" ", "_")
    else:
        return
    
    if should_skip(skip_check):
        print(f"Skipping downloaded image {filename}")
        return
        
    ranking_by_user = image_json.get("ranking_by_user")
    if SKIP_LOW_RATED and ranking_by_user and isinstance(ranking_by_user, int) and (ranking_by_user in [1, 2]):
        # print(f"Skipping low rated image {filename}")
        return
    elif os.path.isfile(f"jobs/{year}/{month}/{image_id}/done") or \
            os.path.isfile(f"jobs/{year}/{month}/{day}/{image_id}/done") or \
            downloaded_previously(image_id):
            # os.path.isfile(f"jobs/{filename}.png") or \
                
        print(f"Skipping downloaded image {filename}")
        return
    else:
        image_path = ensure_path_exists(year, month, day, image_id)
        # image_path = "Rising"
        full_path = f"{image_path}/{filename}.png"
        
        for idx, image_url in enumerate(image_paths):
            if idx > 0:
                filename = f"{filename[:97]}-{idx}"
                full_path = f"{image_path}/{filename}.png"
            opener = urllib.request.build_opener()
            opener.addheaders = [('User-agent', UA)]
            urllib.request.install_opener(opener)
            urllib.request.urlretrieve(image_url, full_path)
        # completed_file_path = f"{image_path}/done"
        # f = open(completed_file_path, "x")
        # f.close()
    return full_path


def paginated_download(order_by="new"):
    page = 1
    page_of_results = get_api_page(order_by, page)
    while page_of_results:
        if isinstance(page_of_results, list) and len(page_of_results) > 0 and "no jobs" in page_of_results[0].get("msg", "").lower():
            print("Reached end of available results")
            break
        str = order_by
        if str == "top-all":
            str = "top"
        print(f"Downloading page #{page} (order by '{str}')")
        download_page(page_of_results)
        page += 1
        page_of_results = get_api_page(order_by, page)


def download_all_order_by_types():
    for order_by_type in ORDER_BY_OPTIONS:
        paginated_download(order_by_type)


def main():
    if not SESSION_TOKEN or not USER_ID:
        raise Exception("Please edit SESSION_TOKEN and USER_ID")
    

    download_all_order_by_types()


if __name__ == "__main__":
    main()