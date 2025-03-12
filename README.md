# Solana Crawler
<img src="./assets/cover.jpg">
<br><br>
<img alt="GitHub Tag" src="https://img.shields.io/github/v/tag/paoloechoes/solana-crawler?label=version&color=green">
<br><br>

This project provides a tool to visualize Solana account transactions. It fetches transaction data for a given Solana address and displays it as a network graph which can be recursevly explored.

## Prerequisites
* **Python**: >=3.13
* **Poetry**: >=2.0.1

## Installation

```bash
git clone https://github.com/paoloechoes/solana-crawler.git && cd solana-crawler && chmod +x ./install && ./install.sh
```

## Installation (Manual)

1.  Clone the repository.
2.  Navigate to the project directory.
3.  Run the installation script:

    ```bash
    ./install.sh
    ```

    This script will:

    * Install the project dependencies using `poetry install`. 
    * Make the crawler script executable. 
    * Create a symlink to the crawler script in `~/.local/bin/`.
    * Update your shell configuration (sourcing `~/.bashrc` or `~/.zshrc`).

## How to Use

1.  Run the crawler script:

    ```bash
    solana-crawler <Solana_address>
    ```

    This will start a local server and open a web browser with the transaction graph for the given Solana address.

## Example

```bash
solana-crawler HPCdHgyku9pmWQKPCM9NMpX9rmWmS2mTpxuKTKKAQc4x
```

<img src="./assets/Screenshot 2025-03-12 at 09.21.21.png">

This will open the network graph showing by default the latest **10 IN** and **10 OUT** transactions for the give address.

---

You can change the displayed number of transactions to whatever you like(up to reasonable amount) by using the `num` parameter in the URL

<img src="./assets/Screenshot 2025-03-12 at 09.27.42.png">
<img src="./assets/Screenshot 2025-03-12 at 09.28.56.png">

---

Thickness of the edges reflect the relative value of the transaction, meaning thicker lines represent bigger value transaction relative to the other ones.

<img src="./assets/Screenshot 2025-03-12 at 09.29.50.png">

## Author
- [Paolo Anzani]("https://x.com/paoloechoes")
- anzanipaolo.enquires@gmail.com