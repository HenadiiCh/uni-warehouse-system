# OptiStock — Warehouse Inventory Management System

**OptiStock** is a desktop application designed for the accounting, analysis, and optimization of goods stored in warehouses. It automates inventory tracking and provides strategic insights using ABC/XYZ analysis and EOQ models.

## 🎓 Academic Context

This project was developed as a coursework assignment for the **"Object-Oriented Programming" (OOP)** course at **Vinnytsia National Technical University (VNTU)** (2nd Year).

The primary goal of this project was to master OOP principles while adhering to a strict set of technical requirements:

* **GUI:** A full-featured Desktop Application with a Graphical User Interface.
* **UX:** Includes an animated, interactive splash screen upon launch.
* **Data Persistence:** Input data is stored in files/databases or retrieved via Web API.
* **Controls:** The main window features a menu bar and controls optimized for data presentation.
* **CRUD:** The program displays data and allows for editing.
* **OOP Architecture:**
    * Implemented entirely using **Classes**.
    * Includes at least one **Interface** or **Protocol**.
    * Features an **Inheritance Hierarchy**.
    * Demonstrates **Method and Operator Overloading**.
    * Architecture is illustrated via a **Class Diagram**.
* **Version Control:** Source code is hosted and managed on GitHub.

## 💡 The "Real Problem" Approach

Driven by a desire to solve actual industry challenges rather than abstract theoretical tasks, the functional requirements for this application were derived from real-world needs.

I consulted with a professor from the **National University of Kyiv-Mohyla Academy (NaUKMA)**, who provided extensive insight into modern logistics and warehouse management gaps. The "Problem Statement" and business logic (ABC/XYZ analysis, Safety Stock calculations) implemented in this application are direct results of those academic and practical consultations.

## ⚖️ Intellectual Property & Licensing

### The Logo
The **OptiStock logo** included in this repository was created using **Brandmark.io**.
* **Usage Warning:** According to Brandmark's terms of service, if you intend to use this logo for **commercial business purposes**, you must purchase a license from Brandmark.
* **Current Status:** Used here strictly for educational/portfolio demonstration.

### The Code
The source code of this software is **Open Source**.
* I grant permission for this code to be used, modified, and distributed for **any purpose** (educational, personal, or commercial) without restriction.

---

## 📚 Knowledge Base & References

The logic and algorithms implemented in OptiStock are based on the following domain-specific materials and datasets:

### 1. Inventory Management Theory (Core Logic)
* **`ABC analysis запасів.pdf`**: This document provided the mathematical basis for the **ABC Analysis** module. It details the Pareto principle (80/20 rule) and how to categorize stock into groups A (High Value), B (Medium), and C (Low).
* **`логістика запасів.pdf`**: Served as the source for **Inventory Logistics**. It defines the formulas for:
    * **EOQ (Economic Order Quantity):** Wilson's formula implementation.
    * **Safety Stock:** Calculation based on standard deviation.
    * **Replenishment Strategies:** Logic for "Just-in-Time", "Fixed Interval", and "Min-Max" systems.

### 2. Demand Prediction Research (Analytics Context)
* **`A_rule-based_model_for_Seoul_Bike_sharing_demand_p.pdf`** & **`Demand Prediction (1).pdf`**: These academic papers discuss rule-based regression models (like CUBIST) for predicting demand. They influenced the design of the **XYZ Analysis** module, specifically how to handle demand volatility and seasonality.
* **`2022-11-Case-Bike Seoul Market-EN.pdf`**: A business analytics case study that provides context on how external factors (weather, time) influence demand, helping to structure the data models.

### 3. Datasets (Testing & prototyping)
* **`SeoulBikeData.csv`**: A large dataset containing weather and rental info. Used for testing the system's ability to handle large arrays of data and calculate variation coefficients for the XYZ analysis.
* **`JourPeriode.xlsx - JourPeriode.csv`**: An auxiliary dataset used to map specific hours to time periods (Morning, Night, etc.), useful for time-based categorization in analytics.
