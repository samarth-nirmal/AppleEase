# import time
# from playwright.sync_api import sync_playwright
# import json
# import sys

# start_time = time.time()

# MAX_JOBS = 3

# def scrape_jobs(role, experience, location):
#     jobs_list = []
#     job_count = 0  

#     with sync_playwright() as p:
#         browser = p.chromium.launch(channel="chrome", headless=False)
#         page = browser.new_page()

#         # Navigate to Naukri.com
#         page.goto("https://www.naukri.com")
        
#         # Fill search fields
#         page.locator('.qsb >> input').nth(0).fill(role)
#         page.click(".dropdownMainContainer")
#         page.click(f"text={experience}")
#         page.locator('.qsb >> input').nth(2).fill(location)
#         page.click(".qsbSubmit")
#         page.wait_for_timeout(3000)  # Wait for results to load

#         page_number = 1  # Track the page number

#         while job_count < MAX_JOBS:
#             # print(f"🔍 Scraping page {page_number}...")

#             # Scrape job listings
#             job_elements = page.query_selector_all(".srp-jobtuple-wrapper")

#             for job in job_elements:
#                 if job_count >= MAX_JOBS:
#                     break  # Stop if we reach MAX_JOBS

#                 job_id = job.get_attribute("data-job-id") if job.get_attribute("data-job-id") else "N/A"
#                 title = job.query_selector(".title").inner_text() if job.query_selector(".title") else "N/A"
#                 company = job.query_selector(".comp-name").inner_text() if job.query_selector(".comp-name") else "N/A"
#                 exp = job.query_selector(".exp").inner_text() if job.query_selector(".exp") else "N/A"
#                 loc = job.query_selector(".locWdth").inner_text() if job.query_selector(".locWdth") else "N/A"
#                 link = job.query_selector("a.title").get_attribute("href") if job.query_selector("a.title") else None

#                 # Visit job details page if link exists
#                 description = "N/A"
#                 if link:
#                     with browser.new_page() as job_page:
#                         job_page.goto(link)
#                         job_page.wait_for_timeout(2000)  # Wait for job details to load
#                         description_element = job_page.query_selector(".styles_JDC__dang-inner-html__h0K4t")
#                         if description_element:
#                             description = description_element.inner_text()

#                 jobs_list.append({
#                     "Job ID": job_id,
#                     "Title": title,
#                     "Company": company,
#                     "Experience": exp,
#                     "Location": loc,
#                     "Link": link,
#                     "Description": description
#                 })

#                 job_count += 1  # Increment job count

#             # Stop if we have collected enough jobs
#             if job_count >= MAX_JOBS:
#                 break

#             # Find the correct "Next" button
#             next_buttons = page.query_selector_all("a.styles_btn-secondary__2AsIP")
#             next_button = None
#             for btn in next_buttons:
#                 if btn.inner_text().strip().lower() == "next":
#                     next_button = btn
#                     break

#             if next_button and next_button.is_visible():
#                 next_button.click()
#                 page.wait_for_timeout(5000)  # Wait for new page to load
#                 page_number += 1
#             else:
#                 # print("🚀 No more pages. Scraping complete.")
#                 break

#         # Close browser
#         browser.close()
#         print(json.dumps(jobs_list, ensure_ascii=False))
        
#     # Save to JSON file
#     with open("naukri_jobs.json", "w", encoding="utf-8") as json_file:
#         json.dump(jobs_list, json_file, indent=4, ensure_ascii=False)

#     # End time
#     end_time = time.time()
#     runtime = end_time - start_time

#     # print(f"✅ Jobs saved to naukri_jobs.json")
#     # print(f"⏳ Total runtime: {runtime:.2f} seconds")
#     # print(f"📊 Total jobs collected: {job_count}")

#     return json.dumps(jobs_list, indent=4, ensure_ascii=False)

# # Entry point for script execution
# if __name__ == "__main__":
#     job_role = sys.argv[1]
#     experience = sys.argv[2]
#     location = sys.argv[3]
#     result = scrape_jobs(job_role, experience, location)



# import time
# from playwright.sync_api import sync_playwright
# import json
# import sys
# import os
# import hashlib

# start_time = time.time()
# MAX_JOBS = 3  # Limit job scraping
# BASE_SESSION_DIR = "naukri_sessions"  # Directory to store user sessions

# # Function to generate user-specific session directory
# def get_user_data_dir(user_id):
#     user_hash = hashlib.md5(user_id.encode()).hexdigest()
#     return os.path.abspath(os.path.join(BASE_SESSION_DIR, user_hash))

# # Function to handle login and save session
# def naukri_login(page):
#     page.goto("https://www.naukri.com/mnjuser/homepage", timeout=10000)
#     #page.wait_for_load_state("networkidle")

#     # Check if already logged in
#     if page.query_selector(".user-details-inner"):
#         print("✅ Already logged in! Proceeding with job scraping...")
#         return

#     print("🔑 Please log in manually...")
    
#     try:
#         page.wait_for_selector(".user-details-inner, #logoutLink", timeout=3000)
#         print("✅ Login detected! Session saved.")
#     except Exception as e:
#         print(f"⚠️ Login detection failed: {e}")

# # Function to scrape jobs
# def scrape_jobs(user_id, role, experience, location):
#     jobs_list = []
#     job_count = 0  

#     user_data_dir = get_user_data_dir(user_id)
#     os.makedirs(user_data_dir, exist_ok=True)  # Ensure session directory exists

#     with sync_playwright() as p:
#         browser = p.chromium.launch_persistent_context(
#             user_data_dir, 
#             channel="chrome",
#             headless=False
#         )
#         page = browser.new_page()

#         # Perform login (session is reused)
#         naukri_login(page)

# # Navigate to Naukri job search page
#         page.goto("https://www.naukri.com")

#         # Fill search fields
#         page.click(".nI-gNb-sb__main")
#         page.locator('.nI-gNb-sb__main >> input').nth(0).fill(role)
#         page.click(".dropdownMainContainer")
#         page.click(f"text={experience}")
#         page.locator('.nI-gNb-sb__main >> input').nth(2).fill(location)
#         page.click(".nI-gNb-sb__icon-wrapper")
#         page.wait_for_timeout(3000)  # Wait for results to load

#         page_number = 1  # Track page number

#         while job_count < MAX_JOBS:
#             job_elements = page.query_selector_all(".srp-jobtuple-wrapper")

#             for job in job_elements:
#                 if job_count >= MAX_JOBS:
#                     break

#                 job_id = job.get_attribute("data-job-id") or "N/A"
#                 title = job.query_selector(".title").inner_text() if job.query_selector(".title") else "N/A"
#                 company = job.query_selector(".comp-name").inner_text() if job.query_selector(".comp-name") else "N/A"
#                 exp = job.query_selector(".exp").inner_text() if job.query_selector(".exp") else "N/A"
#                 loc = job.query_selector(".locWdth").inner_text() if job.query_selector(".locWdth") else "N/A"
#                 link = job.query_selector("a.title").get_attribute("href") if job.query_selector("a.title") else None

#                 # Visit job details page if link exists
#                 description = "N/A"
#                 if link:
#                     with browser.new_page() as job_page:
#                         job_page.goto(link)
#                         job_page.wait_for_timeout(2000)
#                         description_element = job_page.query_selector(".styles_JDC__dang-inner-html__h0K4t")
#                         if description_element:
#                             description = description_element.inner_text()

#                 jobs_list.append({
#                     "Job ID": job_id,
#                     "Title": title,
#                     "Company": company,
#                     "Experience": exp,
#                     "Location": loc,
#                     "Link": link,
#                     "Description": description
#                 })

#                 job_count += 1  

#             if job_count >= MAX_JOBS:
#                 break

#             # Find and click "Next" button
#             next_buttons = page.query_selector_all("a.styles_btn-secondary__2AsIP")
#             next_button = None
#             for btn in next_buttons:
#                 if btn.inner_text().strip().lower() == "next":
#                     next_button = btn
#                     break

#             if next_button and next_button.is_visible():
#                 next_button.click()
#                 page.wait_for_timeout(5000)  
#                 page_number += 1
#             else:
#                 break

#         browser.close()
#         print(json.dumps(jobs_list, ensure_ascii=False))

#     # Save to JSON file
#     with open(f"naukri_jobs_{user_id}.json", "w", encoding="utf-8") as json_file:
#         json.dump(jobs_list, json_file, indent=4, ensure_ascii=False)

#     end_time = time.time()
#     runtime = end_time - start_time

#     return json.dumps(jobs_list, indent=4, ensure_ascii=False)

# # Entry point
# if __name__ == "__main__":
#     user_id = sys.argv[1]
#     job_role = sys.argv[2]
#     experience = sys.argv[3]
#     location = sys.argv[4]
#     result = scrape_jobs(user_id, job_role, experience, location)


import time
import json
import sys
import os
import hashlib
from playwright.sync_api import sync_playwright
from naukri_login import get_user_data_dir

start_time = time.time()
def is_logged_in(page):

    page.goto("https://www.naukri.com/mnjuser/homepage", timeout=10000)
    return bool(page.query_selector(".user-details-inner"))

def scrape_jobs(user_id, role, experience, location, noOfJobs):
    MAX_JOBS = int(noOfJobs)
    jobs_list = []
    job_count = 0  

    user_data_dir = get_user_data_dir(user_id)
    if not os.path.exists(user_data_dir):
        print("⚠️ No session found! Please log in first using `naukri_login.py`.")
        return json.dumps([])

    with sync_playwright() as p:
        browser = p.chromium.launch_persistent_context(
            user_data_dir, 
            channel="chrome",
            headless=False
        )
        page = browser.new_page()

        # Check if already logged in
        if not is_logged_in(page):
            print("⚠️ User not logged in! Please log in first using `naukri_login.py`.")
            browser.close()
            return json.dumps([])

       
        page.goto("https://www.naukri.com")
        page.click(".nI-gNb-sb__main")
        page.locator('.nI-gNb-sb__main >> input').nth(0).fill(role)
        page.click(".dropdownMainContainer")
        page.click(f"text={experience}")
        page.locator('.nI-gNb-sb__main >> input').nth(2).fill(location)
        page.click(".nI-gNb-sb__icon-wrapper")
        page.wait_for_timeout(3000) 

        page_number = 1 

        while job_count < MAX_JOBS:
            job_elements = page.query_selector_all(".srp-jobtuple-wrapper")

            for job in job_elements:
                if job_count >= MAX_JOBS:
                    break

                job_id = job.get_attribute("data-job-id") or "N/A"
                title = job.query_selector(".title").inner_text() if job.query_selector(".title") else "N/A"
                company = job.query_selector(".comp-name").inner_text() if job.query_selector(".comp-name") else "N/A"
                exp = job.query_selector(".exp").inner_text() if job.query_selector(".exp") else "N/A"
                loc = job.query_selector(".locWdth").inner_text() if job.query_selector(".locWdth") else "N/A"
                link = job.query_selector("a.title").get_attribute("href") if job.query_selector("a.title") else None

                
                description = "N/A"
                if link:
                    with browser.new_page() as job_page:
                        job_page.goto(link)
                        job_page.wait_for_timeout(2000)
                        description_element = job_page.query_selector(".styles_JDC__dang-inner-html__h0K4t")
                        if description_element:
                            description = description_element.inner_text()

                jobs_list.append({
                    "jobId": job_id,
                    "jobTitle": title,
                    "companyName": company,
                    "experienceRequired": exp,
                    "Location": loc,
                    "Link": link,
                    "jobDescription": description
                })

                job_count += 1  

            if job_count >= MAX_JOBS:
                break

            
            next_buttons = page.query_selector_all("a.styles_btn-secondary__2AsIP")
            next_button = None
            for btn in next_buttons:
                if btn.inner_text().strip().lower() == "next":
                    next_button = btn
                    break

            if next_button and next_button.is_visible():
                next_button.click()
                page.wait_for_timeout(5000)  
                page_number += 1
            else:
                break

        browser.close()
        print(json.dumps(jobs_list, ensure_ascii=False))


# Entry point
if __name__ == "__main__":
    user_id = sys.argv[1]
    job_role = sys.argv[2]
    experience = sys.argv[3]
    location = sys.argv[4]
    noOfJobs = sys.argv[5]
    result = scrape_jobs(user_id, job_role, experience, location, noOfJobs)
