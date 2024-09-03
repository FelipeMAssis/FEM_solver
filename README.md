# FEM Model Analysis

This repository contains a finite element model (FEM) analysis framework. It allows users to define nodes, materials, properties, elements, constraints, and loads, then run simulations and visualize results.

## Table of Contents

- [Installation](#installation)
- [Usage](#usage)
  - [Test Script](#test-script)
  - [Interactive Script](#interactive-script)
- [Example Input](#example-input)
- [Contributing](#contributing)
- [License](#license)

## Installation

To use this FEM analysis framework, follow these steps:

1. **Clone the repository:**

    ```bash
    git clone https://github.com/FelipeMAssis/FEM_solver.git
    cd FEM_solver
    ```

2. **Install dependencies:**

    You can install the required packages using the provided requirements.txt file. First, ensure you have Python 3.12 installed, then run:

    ```bash
    pip install -r requirements.txt
    ```

    Alternatively, you can install the packages manually:

    ```bash
    pip install numpy matplotlib
    ```

3. **Set up the repository:**

    The repository is structured into modules for nodes, elements, materials, properties, boundary conditions, and models.

## Usage

### Test Script

The test_script.py file contains a predefined test case for verifying the FEM implementation. To run the test script, use:

```bash
python test_script.py
```

This script will execute a predefined FEM problem and display the displacements and plot the results.

### Interactive Script

The main.py file allows users to input their own parameters to define nodes, materials, properties, elements, constraints, and loads. To run the interactive script, use:

```bash
python main.py
```

Follow the prompts to enter your problem parameters. The script will perform the FEM analysis and display the displacements and plot the results.

## Contributing

Contributions are welcome! Please follow these steps:

1. Fork the repository.
2. Create a feature branch.
3. Commit your changes.
4. Push to the feature branch.
5. Open a pull request.
Please ensure that your code adheres to the existing style and includes tests for new features.







