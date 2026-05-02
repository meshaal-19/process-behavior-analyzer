# Process Behavior Analyzer

A real-time system monitoring tool that tracks CPU and memory usage of running processes and detects anomalies using time-based analysis instead of single snapshots.

---

## Overview

This project analyzes process behavior over time to identify sustained anomalies such as high CPU usage and continuous memory growth.

Unlike traditional monitoring tools that rely on instantaneous readings, this system uses **consecutive interval analysis** to distinguish between transient spikes and persistent abnormal behavior.

---

## Key Features

- Real-time monitoring of CPU and memory usage for active processes  
- Time-based anomaly detection using consecutive interval tracking  
- Detection of sustained high CPU usage  
- Detection of continuous memory growth patterns  
- Logging of anomalous processes with timestamps  
- Visualization of CPU and memory trends over time  

---

## How It Works

1. Continuously samples CPU and memory usage of all running processes  
2. Tracks changes across multiple time intervals  
3. Flags processes when thresholds are exceeded consistently  
4. Logs anomalies and stores data for flagged processes  
5. Generates graphs showing CPU and memory behavior over time  

---

## Tech Stack

- Python  
- psutil (system monitoring)  
- matplotlib (data visualization)  

---

## How to Run

1. Install dependencies:

```bash
pip install -r requirements.txt
```

2. Run the program:
   ```bash
   python monitor.py
   ```

3.Stop execution:
Press Ctrl + C to stop monitoring and generate results

Sample Output

Example of detected anomalies from real system monitoring:
 [View Log Output](./sample_log.txt)


   

