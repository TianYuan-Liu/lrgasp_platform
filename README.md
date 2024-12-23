# LongTREC-LRGASP Platform

A comprehensive web platform for systematic assessment of long-read RNA-seq methods for transcript identification and quantification.

## Overview

The **LongTREC-LRGASP Platform** provides a collaborative environment for researchers to:
- Submit predictions for transcript identification and quantification.
- Access benchmark datasets tailored for RNA-seq evaluations.
- Participate in structured evaluation challenges.
- Compare results and metrics with other participants for enhanced insights.

## Features

### 🏆 Challenge Management
The platform supports three distinct challenges in RNA-seq analysis:
1. **Challenge 1**: Reconstructing full-length transcripts.
2. **Challenge 2**: Quantifying transcript abundance.
3. **Challenge 3**: De novo transcript reconstruction.

### 📂 Data Access
Curated datasets include:
- **Human (WTC11)**: Comprehensive transcriptomic data from the human WTC11 cell line.
- **Mouse ES Cells**: High-quality RNA-seq data for benchmarking.
- **Manatee Leukocytes**: Unique dataset for diverse transcriptomics evaluations.

### ⚙️ Automated Evaluation
Submissions are processed with real-time feedback, providing detailed performance metrics.

---

## Installation

### 1️⃣ Clone the Repository
```bash
git clone https://github.com/your-repo/LRGASP-Platform.git
cd LRGASP-Platform
```

### 2️⃣ Set Up a Virtual Environment
```bash
python -m venv venv
source venv/bin/activate  # For Linux/Mac
venv\Scripts\activate     # For Windows
```

### 3️⃣ Install Dependencies
```bash
pip install -r requirements.txt
```

### 4️⃣ Run the Development Server
```bash
flask run
```

## Usage
- **Register** for an account via the platform's web interface.
- Browse **available challenges** and associated datasets.
- **Submit predictions** through the upload interface.
- Access **automated evaluation results** for real-time insights.
---

## Contributing
We welcome contributions to the LongTREC-LRGASP Platform. Please follow these steps:
1. **Fork** the repository and create a new branch for your feature (e.g. new benchmarking datasets, benchmarking matrices) or bug fix.
2. **Commit** and push your changes to your fork.
3. **Submit a pull request** for review.



