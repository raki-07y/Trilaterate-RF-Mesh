# Trilaterate-RF-Mesh

An open-source localization engine designed to compute the real-time positions of mobile target nodes traversing a Radio Frequency (RF) Mesh network. By taking Received Signal Strength Indication (RSSI) data or Time-of-Flight (ToF) metrics from multiple fixed reference nodes (anchors), this project implements Trilateration and Multilateration algorithms to accurately map coordinates.

## 📌 Features

- **Trilateration Engine**: Resolves the intersection of overlapping distance boundaries across 3 or more fixed anchor points.
- **Signal-to-Distance Modeling**: Built-in conversion modules utilizing the Log-Distance Path Loss model to translate RSSI (dBm) into meters.
- **Error Minimization**: Implements Least Squares Approximation (or alternative optimization models like Gauss-Newton) to mitigate RF multi-path interference and environmental noise.
- **Dynamic Mesh Support**: Scales from simple 3-anchor 2D systems to complex N-anchor arrays.

## 📐 How It Works

Trilateration works by measuring distances from a series of known coordinate reference anchors ($A_1, A_2, A_3$) to an unknown tracking node ($T$).

### Distance Estimation
The software captures incoming RF signals from the mesh, estimating the distance ($r_n$) using:
$$\text{RSSI} = -10n \log_{10}(d) + A$$

### Intersection Calculation
Formulates system equations representing circles (2D) or spheres (3D) around each anchor.

### Optimization
Resolves the coordinates $(x, y)$ of the target where the geometric paths intersect, smoothing out signal fluctuations via a mathematical optimization loop.

## 🚀 Getting Started

### Prerequisites

Depending on your implementation stack (Python / Node.js / C++), ensure you have the appropriate runtime installed. For a typical Python-based optimization engine:

```bash
pip install numpy scipy matplotlib
```

### Installation

1. Clone the repository:

```bash
git clone https://github.com/raki-07y/Trilaterate-RF-Mesh.git
cd Trilaterate-RF-Mesh
```

2. Configure your anchor nodes setup in the configuration file (e.g., `config.json` or within the main script):

```json
{
  "anchors": [
    {"id": "A1", "x": 0.0,  "y": 0.0},
    {"id": "A2", "x": 10.0, "y": 0.0},
    {"id": "A3", "x": 5.0,  "y": 8.66}
  ]
}
```

### Running the System

Execute the core algorithm processing script:

```bash
python main.py
```

## 📂 Repository Structure

```
Trilaterate-RF-Mesh/
├── src/                       # Core algorithms & processing engine
│   ├── trilateration.py       # Matrix operations and intersection geometry
│   ├── path_loss.py           # RSSI-to-distance conversion utilities
│   └── mesh_handler.py        # Handles multi-node network packets
├── config/                    # Network layout configurations
├── simulations/               # Test scripts for synthetic data evaluation
├── LICENSE                    # MIT License
└── README.md                  # Project overview
```

## 🛠️ Future Enhancements

- [ ] Support for Extended Kalman Filters (EKF) to smooth sequential tracking pathways
- [ ] Direct hardware integration profiles (e.g., ESP32, nRF52, UWB modules)
- [ ] Real-time web visualization dashboard mapping tracking history

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
