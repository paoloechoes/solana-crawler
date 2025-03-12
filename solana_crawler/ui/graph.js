function initGraph(graphNodes, graphEdges, dfIn, dfOut) {

    /**
     * Graph Setup
     */
    const nodes = new vis.DataSet(graphNodes);
    const edges = new vis.DataSet(graphEdges);
    const df_in = dfIn;
    const df_out = dfOut;

    const container = document.getElementById('graph');
    const data = { nodes: nodes, edges: edges };

    const options = {
        layout: {
            improvedLayout: true,
        },
        physics: {
            enabled: true,
            solver: 'repulsion',
            repulsion: {
                nodeDistance: 300,
                springLength: 200,
                damping: 0.09
            },
            stabilization: {
                enabled: true,
                iterations: 200,
                updateInterval: 25
            }
        },
        edges: {
            arrows: 'to',
            smooth: {
                type: 'dynamic'
            },
            scaling: {
                min: 1,
                max: 10
            }
        },
        nodes: {
            shape: 'ellipse',
            font: {
                size: 14,
                color: '#000'
            },
            scaling: {
                label: true
            }
        },
        interaction: {
            dragNodes: true,
            zoomView: true,
            dragView: true
        }
    };

    // Render Graph
    const network = new vis.Network(container, data, options);

    network.on("selectEdge", function (params) {
        if (params.edges.length > 0) {
            const tbody = document.querySelector("#transactionTable tbody");
            tbody.innerHTML = "";

            const uniqueTransactions = new Set();

            params.edges.forEach((edge) => {
                const edgeId = edge; 

                let transactions = [];
                if (edges.get(edgeId).label === "in") {
                    transactions = df_in.filter(tx => tx.from_address === edges.get(edgeId).from);
                } else if (edges.get(edgeId).label === "out") {
                    transactions = df_out.filter(tx => tx.to_address === edges.get(edgeId).to);
                }

                transactions.forEach((transactionData) => {
                    const uniqueKey = `${transactionData.block_time}-${transactionData.from_address}-${transactionData.to_address}`;
                    if(!uniqueTransactions.has(uniqueKey)) {
                        uniqueTransactions.add(uniqueKey);
                        const row = document.createElement("tr");
                        row.innerHTML = `
                            <td>${transactionData.block_time}</td>
                            <td><a href="${transactionData.from_address}">${transactionData.from_address || "-"}</a></td>
                            <td><a href="${transactionData.to_address}">${transactionData.to_address || "-"}</a></td>
                            <td><a href="https://solscan.io/token/${transactionData.token_address}">${transactionData.token_address}</a></td>
                            <td>${transactionData.amount / 10**transactionData.token_decimals}</td>
                            <td>${transactionData.value}</td>`;
                        tbody.appendChild(row);
                    }
                });
            });
        }
    });

    /**
     * Controls Section
     */

    document.getElementById('loadedEdges').textContent = `Loaded Edges: ${data.edges.length}`
    document.getElementById('loadedNodes').textContent = `Loaded Nodes: ${data.nodes.length}`

    network.on("selectNode", function(params) {
        document.querySelector('#selectedNode > a').setAttribute('href', params.nodes[0]);
        document.querySelector('#selectedNode > a').textContent = params.nodes[0];

        document.querySelector('#viewOnSolscan > a').setAttribute('href', `https://solscan.io/account/${params.nodes[0]}`);
        document.querySelector('#viewOnSolscan > a').textContent = '(view on Solscan)';
    });

    // Turn ON/OFF Edges
    function toggleEdges() {
        const showIn = document.getElementById('toggleIn').checked;
        const showOut = document.getElementById('toggleOut').checked;

        edges.forEach(edge => {
            if (edge.label === 'in') {
                edges.update({ id: edge.id, hidden: !showIn });
            } else if (edge.label === 'out') {
                edges.update({ id: edge.id, hidden: !showOut });
            }
        });
    }
    document.getElementById('toggleIn').addEventListener('change', toggleEdges);
    document.getElementById('toggleOut').addEventListener('change', toggleEdges);


    // Dark Mode
    const toggleButton = document.getElementById('toggle-button');
    const body = document.body;

    const darkMode = localStorage.getItem('darkMode');
    if (darkMode === 'true') {
        body.classList.add('dark-mode');
        toggleButton.textContent = 'Light Mode';
    }

    toggleButton.onclick = function() {
        body.classList.toggle('dark-mode');
        toggleButton.textContent = body.classList.contains('dark-mode') ? 'Light Mode' : 'Dark Mode';
        localStorage.setItem('darkMode', body.classList.contains('dark-mode'));
    }
}
