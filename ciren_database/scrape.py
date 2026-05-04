"""
Downloads the .xlsx case data for each cirenid
"""
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import time
import os


# Leave blank to use Chrome's default download folder.
# Fill in an absolute path, for example: r"D:\UMich\Senior Year\umtri\ciren_database\downloads"
DOWNLOAD_FOLDER = rf"D:\UMich\Senior Year\umtri\ciren_database\CrashExports"

options = Options()
options.add_argument("--log-level=3")
options.add_experimental_option("excludeSwitches", ["enable-logging"])
if DOWNLOAD_FOLDER:
    os.makedirs(DOWNLOAD_FOLDER, exist_ok=True)
    options.add_experimental_option(
        "prefs",
        {
            "download.default_directory": os.path.abspath(DOWNLOAD_FOLDER),
            "download.prompt_for_download": False,
            "download.directory_upgrade": True,
        },
    )

driver = webdriver.Chrome(options=options)

cirenids1 = [11, 15, 16, 17, 19, 20, 28, 30, 31, 34, 35, 39, 41, 42, 43, 45, 49, 51, 56, 57, 58, 63, 64, 66, 67, 68, 69, 73, 76, 77, 78, 80, 84, 89, 90, 91, 92, 95, 98, 99, 100, 102, 103, 104, 105, 110, 112, 115, 117, 119, 123, 132, 133, 134, 135, 136, 138, 139, 141, 145, 150, 158, 160, 161, 162, 164, 180, 181, 189, 193, 194, 195, 197, 198, 200, 201, 211, 214, 216, 220, 221, 226, 227, 229, 230, 231, 244, 248, 251, 253, 258, 262, 266, 267, 274, 287, 290, 291, 298, 299]
cirenids2 = [303, 310, 311, 324, 341, 350, 351, 352, 359, 363, 398, 406, 408, 409, 417, 420, 421, 424, 426, 427, 428, 432, 433, 434, 439, 440, 444, 459, 460, 465, 479, 490, 497, 518, 527, 533, 536, 537, 542, 550, 555, 557, 558, 559, 567, 580, 581, 584, 590, 594, 597, 623, 634, 653, 658, 661, 664, 665, 666, 678, 681, 687, 702, 704, 708, 709, 718, 725, 730, 731, 732, 733, 740, 742, 743, 748, 759, 760, 761, 769, 783, 798, 800, 802, 804, 805, 806, 811, 814, 816, 818, 819, 824, 826, 827, 828, 853, 854, 866, 868]
cirenids3 = [871, 882, 883, 897, 898, 915, 916, 923, 938, 945, 948, 962, 963, 972, 977, 980, 982, 984, 990, 1010, 1034, 1047, 1056, 1070, 1078, 1088, 1089, 1094, 1098, 1101, 1124, 1125, 1148, 1149, 1157, 1216, 1217, 1245, 980015, 980018, 980019, 980020, 980024, 980035, 980038, 980039, 980052, 980054, 980090, 980091, 980103, 980112, 980113, 980114, 980119, 980121, 980122, 980145, 980146, 980188, 980217, 980340]

cirenids = cirenids1 + cirenids2 + cirenids3

for case_id in cirenids:
    print(f"Processing CIRENID {case_id}")
    case_url = f"https://crashviewer.nhtsa.dot.gov/ciren/details/{case_id}/ciren-summary-document"
    driver.get(case_url)

    try:
        export_btn = WebDriverWait(driver, 5).until(
            EC.element_to_be_clickable(
                (
                    By.XPATH,
                    "//button[contains(normalize-space(.), 'Export Case Data')]",
                )
            )
        )
        driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", export_btn)
        time.sleep(0.5)
        driver.execute_script("arguments[0].click();", export_btn)
        print(f"  Download triggered for {case_id}")
        time.sleep(2.5)
    except TimeoutException:
        print(f"  Skipped {case_id}: export button not found")
    except Exception as exc:
        print(f"  Skipped {case_id}: click failed ({exc})")


driver.quit()
print("Done.")
