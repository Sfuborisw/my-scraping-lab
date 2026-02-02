# my-scraping-lab

# 🛡️ POE2 Market Analysis & Logger (Study Notes)

This project is designed to **automate the recording of POE2 market currency exchange rates** and save the data as a **CSV file** for long-term analysis.

---

## 1️⃣ Step 1: Development Environment Management (venv)

**What is venv?**
A Virtual Environment is like an independent **"sandbox"**. Libraries installed inside (e.g., **Pandas**) won't affect other parts of your computer, ensuring the program runs consistently on any machine.

* **Activate**:
    `source venv/Scripts/activate` (Git Bash)
* **Deactivate**:
    `deactivate`
* **Install Necessary Tools**:
    ```bash
    pip install requests pandas
    ```

---

## 2️⃣ Step 2: Data Detective (How to find the API)

When the POE2 season updates, the API URL might change. Here is the process to find the new URL:

1.  Open Chrome and go to poe.ninja.
2.  Press **F12** to open Developer Tools -> Switch to the **Network** Tab.
3.  Type `overview` or `exchange` in the Filter box.
4.  Refresh the page and find a link returning **JSON** format.
5.  **Key Observation**: Check the data structure in `Preview` to find which field contains the price (e.g., `primaryValue`).

---

## 3️⃣ Step 3: Core Logic Analysis (Mapping & CSV)

### 🧩 Data Mapping
The data fetched from the API usually only has IDs (e.g., `alch`). We use a **Dictionary** to convert them into human-readable names:
```python
id_map = {'alch': 'Alchemy Orb', 'divine': 'Divine Orb'}
name = id_map.get(curr_id, "Unknown")
```

### 📝 Writing to CSV (Logging)
We use the `to_csv` function from Pandas and set `mode='a'` (Append):

*   **If the file does not exist**: Write **Header + Data**.
*   **If the file exists**: Append **data only**, no Header.

---

## 4️⃣ Step 4: Automation & Frequency Control (Wait Time)

To prevent being banned by the website (**IP Ban**), we must set a wait time:

*   **Logic**: Use `while True:` combined with `time.sleep(3600)`.

**Recommended Frequency**:

*   **1 Hour (3600s)**: Safest, suitable for collecting long-term trends.
*   **15 Minutes (900s)**: Suitable for tracking real-time fluctuations.

> **Note**: Never set it to less than **60 seconds**, or it is highly likely to be considered a malicious attack.

---

## 5️⃣ Step 5: Daily Operation Workflow

Every time you want to start recording data, follow these steps:

1.  Open **Git Bash**.
2.  Enter folder: `cd my-scraping-lab`.
3.  Activate venv: `source venv/Scripts/activate`.
4.  Run program: `python poe_analytics.py`.
5.  Finish: Press **Ctrl + C** to stop, then `deactivate` to exit the environment.
