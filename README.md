
# Prediction of Particle Emission Points using Deep Learning

This repository provides a complete framework for predicting **particle emission sources (E1, E2, E3)** in simulated industrial environments using deep learning models based on **temporal sensor data**.

The project explores and compares three architectures:
- **MLP** (Multilayer Perceptron) — static feature baseline;
- **CNN1D** (1D Convolutional Network) — temporal feature extraction;
- **LSTM** (Long Short-Term Memory) — sequential pattern modeling.

---

## Project Structure

```
.
├── data/                  # Input CSVs and intermediate files
│   ├── raw/               # Original unprocessed data
│   ├── processed/         # Processed data ready for training/evaluation
│
├── models/                # Trained Keras models (.h5)
│   ├── cnn1d_model.keras
│   ├── lstm_model.keras
│   └── mlp_model.keras
│
├── results/               # Saved plots and outputs (e.g., importance charts)
│
├── notebooks/
│   ├── model_comparison.ipynb      # Metrics comparison + visualizations
│   ├── cnn_model_training.ipynb    # CNN1D training and evaluation
│   ├── lstm_model_training.ipynb   # LSTM training and evaluation
│   └── mlp_baseline.ipynb          # MLP model baseline
│
└── README.md
```

---

## Installation & Setup

1. **Clone the repository**
```bash
git clone https://github.com/lucasmcmatos/predicition-particle-emission-points.git
cd predicition-particle-emission-points
```

2. **Create virtual environment**
```bash
python -m venv venv
source venv/bin/activate  # (Linux/macOS)
venv\Scripts\activate     # (Windows)
```

3. **Install dependencies**
```bash
pip install -r requirements.txt
```

---

## How to Run

### Train Models

Use the provided notebooks in `notebooks/` to train each model:
- `cnn_model_training.ipynb`
- `lstm_model_training.ipynb`
- `mlp_baseline.ipynb`

> Each notebook is self-contained and includes data loading, model definition, training, and evaluation.

---

### Run Model Comparison

Use `model_comparison.ipynb` to:
- Load saved models;
- Compare metrics;
- Visualize radar plots;
- Analyze variable importance using occlusion sensitivity.

Output plots will be saved in the `results/` folder.

---

## Dataset Format

For CNN1D/LSTM models, data should be pre-processed into **flattened temporal windows**:

- **Shape**: `(N, window_size × num_sensors)`
- **Label column**: `"target"`  
- Use the script or notebook cells to reshape into `(N, window_size, num_sensors)`.

---

## Results

The best models achieved:
- **CNN1D**: ~95.7% accuracy
- **LSTM**: ~95.7% accuracy
- **MLP**: ~28% accuracy

CNN1D and LSTM significantly outperformed MLP by leveraging temporal sensor patterns.

---

## Highlights

- Reproducible training pipelines;
- Variable importance via Occlusion Sensitivity;
- Scientific reporting-ready charts and metrics;
- Suitable for academic publication and industrial deployment.

---

## 🧑‍💻 Author

**Lucas Matos**  
[GitHub](https://github.com/lucasmcmatos) | [LinkedIn](https://www.linkedin.com/in/lucas-m-c-matos-014879222/)

---
