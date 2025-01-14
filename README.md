# GitHub Issue Mining and Contributor Activity Analysis

## Overview

This project involves extracting and analyzing issue reports from the [Apache Doris GitHub repository](https://github.com/apache/doris) to study contributor activity. Using the PyGitHub library and Python, the project focuses on identifying and sorting contributors based on their activity in terms of issue submissions, with visualizations showcasing the findings.

## Objectives

- Extract closed issue reports from the Apache Doris GitHub repository.
- Identify the contributors who submitted the issues and their activity levels.
- Analyze the number of issues submitted by each contributor and determine trends based on monthly averages.
- Visualize the sorted data to showcase the most active contributors from January 2022 to March 2024.

## Key Features

- **Data Extraction**: Used PyGitHub to pull data from the Apache Doris GitHub repository.
- **Sorting Metrics**: Sorted contributors based on:
  - Total number of issues submitted.
  - Average number of issues submitted per month.
  - Monthly issue submissions from January 2022 to March 2024.
- **Data Visualization**: Plotted the sorted contributor activity using Matplotlib for better presentation of the findings.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-username/github-issue-mining.git
