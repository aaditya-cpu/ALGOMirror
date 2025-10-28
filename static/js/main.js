// static/js/main.js

document.addEventListener('DOMContentLoaded', () => {
    // =================================================================
    // 1. STATE MANAGEMENT & INITIALIZATION
    // =================================================================
    let ALL_CONTENT = {};
    let currentData = null;
    let currentDataType = 'array'; // Default on load
    const animator = new Animator(
        'visualization-container',
        'aux-visualization-container',
        'status-log',
        'speed-slider'
    );

    // --- DOM ELEMENT REFERENCES ---
    // A single object to hold all UI element references for clean access
    const UI = {
        dsSelect: document.getElementById('ds-select'),
        algoSelect: document.getElementById('algo-select'),
        dataSizeInput: document.getElementById('data-size'),
        runBtn: document.getElementById('run-btn'),
        generationControls: document.getElementById('generation-controls'),
        // Input groups that are shown/hidden contextually
        targetInputGroup: document.getElementById('target-input-group'),
        targetValueInput: document.getElementById('target-value'),
        startNodeGroup: document.getElementById('start-node-group'),
        startNodeSelect: document.getElementById('start-node-select'),
        endNodeGroup: document.getElementById('end-node-group'),
        endNodeSelect: document.getElementById('end-node-select'),
        // Info panel elements
        info: {
            title: document.getElementById('info-title'),
            idea: document.getElementById('info-idea'),
            pseudo: document.getElementById('info-pseudo'),
            timeBest: document.getElementById('time-best'),
            timeAvg: document.getElementById('time-avg'),
            timeWorst: document.getElementById('time-worst'),
            spaceWorst: document.getElementById('space-worst'),
        }
    };

    /**
     * Kicks off the application by fetching content and setting up the initial UI.
     */
    async function initialize() {
        try {
            const response = await fetch('/get_content');
            ALL_CONTENT = await response.json();
            populateDataStructureSelect();
            handleDataStructureChange(); // Set up UI for the default selection
        } catch (error) {
            console.error("Fatal Error: Could not load initial content from server.", error);
            animator.updateLog("Error: Connection to the server failed. Please refresh the page.");
        }
    }

    // =================================================================
    // 2. UI UPDATE & MANAGEMENT
    // =================================================================

    function populateDataStructureSelect() {
        UI.dsSelect.innerHTML = '';
        Object.keys(ALL_CONTENT.data_structures).forEach(dsKey => {
            const hasAlgos = Object.values(ALL_CONTENT.algorithms).some(algo => algo.ds === dsKey);
            if (hasAlgos) {
                const ds = ALL_CONTENT.data_structures[dsKey];
                const option = document.createElement('option');
                option.value = dsKey;
                option.textContent = ds.name;
                UI.dsSelect.appendChild(option);
            }
        });
    }

    function populateAlgoSelect() {
        const selectedDs = UI.dsSelect.value;
        UI.algoSelect.innerHTML = '';
        Object.keys(ALL_CONTENT.algorithms).forEach(key => {
            if (ALL_CONTENT.algorithms[key].ds === selectedDs) {
                const algo = ALL_CONTENT.algorithms[key];
                const option = document.createElement('option');
                option.value = key;
                option.textContent = algo.name;
                UI.algoSelect.appendChild(option);
            }
        });
        handleAlgorithmChange();
    }

    function updateGenerationControls() {
        UI.generationControls.querySelectorAll('button').forEach(btn => btn.style.display = 'none');
        // The 'data-size' input label should be context-aware
        const sizeLabel = document.querySelector('label[for="data-size"]');

        switch (currentDataType) {
            case 'array':
                document.getElementById('generate-random-array-btn').style.display = 'block';
                document.getElementById('generate-sorted-array-btn').style.display = 'block';
                sizeLabel.textContent = "Array Size:";
                break;
            case 'tree':
                document.getElementById('generate-tree-btn').style.display = 'block';
                sizeLabel.textContent = "Number of Nodes:";
                break;
            case 'graph':
                document.getElementById('generate-graph-btn').style.display = 'block';
                sizeLabel.textContent = "Number of Nodes:";
                break;
            case 'conceptual':
                // For conceptual algorithms, the 'size' input is used for 'N'
                sizeLabel.textContent = "Input N value (e.g., for Fib):";
                break;
        }
    }

    function updateExecutionInputs() {
        const algoKey = UI.algoSelect.value;
        const algo = ALL_CONTENT.algorithms[algoKey];

        // Hide all contextual input fields by default
        UI.targetInputGroup.style.display = 'none';
        UI.startNodeGroup.style.display = 'none';
        UI.endNodeGroup.style.display = 'none';

        // Show inputs based on the algorithm's specific needs
        if (algo?.category === 'Searching') {
            UI.targetInputGroup.style.display = 'block';
        }
        if (['Graph Traversal', 'Shortest Path'].includes(algo?.category)) {
            UI.startNodeGroup.style.display = 'block';
        }
        if (algoKey === 'dijkstra') {
            UI.endNodeGroup.style.display = 'block';
        }
    }

    function updateInfoPanel() {
        const algoKey = UI.algoSelect.value;
        if (!algoKey || !ALL_CONTENT.algorithms[algoKey]) return;
        const content = ALL_CONTENT.algorithms[algoKey];
        UI.info.title.textContent = content.name;
        UI.info.idea.textContent = content.idea;
        UI.info.pseudo.textContent = content.pseudocode.trim();
        UI.info.timeBest.textContent = content.complexity.time_best;
        UI.info.timeAvg.textContent = content.complexity.time_avg;
        UI.info.timeWorst.textContent = content.complexity.time_worst;
        UI.info.spaceWorst.textContent = content.complexity.space;
    }

    function setControlsDisabled(disabled) {
        UI.runBtn.disabled = disabled;
        UI.dsSelect.disabled = disabled;
        UI.algoSelect.disabled = disabled;
        UI.dataSizeInput.disabled = disabled;
        UI.generationControls.querySelectorAll('button').forEach(btn => btn.disabled = disabled);
    }

    // =================================================================
    // 3. EVENT HANDLERS & DATA FLOW
    // =================================================================

    function handleDataStructureChange() {
        currentDataType = UI.dsSelect.value;
        populateAlgoSelect();
        updateGenerationControls();
        if (currentDataType !== 'conceptual') {
            generateData();
        } else {
            // For conceptual types, just clear the board, no data generation needed
            animator.clearAll();
            animator.updateLog("Select a conceptual algorithm and click Run.");
        }
    }

    function handleAlgorithmChange() {
        updateExecutionInputs();
        updateInfoPanel();
    }

    async function generateData(isSorted = false) {
        setControlsDisabled(true);
        animator.updateLog(`Generating ${currentDataType}...`);
        try {
            const response = await fetch('/generate_data', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ size: UI.dataSizeInput.value, dtype: currentDataType, sorted: isSorted })
            });
            currentData = await response.json();
            animator.drawInitialState(currentDataType, currentData);
            animator.updateLog("New data generated. Ready to run an algorithm.");

            if (currentDataType === 'graph' && currentData.nodes) {
                UI.startNodeSelect.innerHTML = '';
                UI.endNodeSelect.innerHTML = '';
                Object.keys(currentData.nodes).sort().forEach(nodeId => {
                    const option = document.createElement('option');
                    option.value = nodeId;
                    option.textContent = `Node ${nodeId}`;
                    UI.startNodeSelect.appendChild(option.cloneNode(true));
                    UI.endNodeSelect.appendChild(option);
                });
            }
        } catch (error) {
            console.error("Failed to generate data:", error);
            animator.updateLog("Error: Could not generate data from server.");
        } finally {
            setControlsDisabled(false);
        }
    }

    async function runAlgorithm() {
        const algoKey = UI.algoSelect.value;
        const algoInfo = ALL_CONTENT.algorithms[algoKey];
        if (!algoInfo) return;

        // Initialize parameters for the API call
        const params = { algorithm: algoKey };

        // Handle parameter gathering based on algorithm type
        // This is a much more robust way to build the params object
        switch (algoInfo.ds) {
            case 'array':
            case 'tree':
            case 'graph':
                if (!currentData) {
                    animator.updateLog("Please generate data first.");
                    return;
                }
                params.input_data = currentData;
                if (algoInfo.category === 'Searching') {
                    if (!UI.targetValueInput.value) {
                        animator.updateLog("Please enter a target value.");
                        return;
                    }
                    params.target = UI.targetValueInput.value;
                }
                if (['Graph Traversal', 'Shortest Path'].includes(algoInfo.category)) {
                    params.start_node = UI.startNodeSelect.value;
                }
                if (algoKey === 'dijkstra') {
                    params.end_node = UI.endNodeSelect.value;
                }
                break;

            case 'conceptual':
                // For conceptual algorithms, we take 'N' from the main size input
                const nValue = UI.dataSizeInput.value;
                if (!nValue || nValue < 0) {
                    animator.updateLog("Please enter a valid non-negative N value.");
                    return;
                }
                params.n = nValue;
                // Note: More complex conceptual algos (Knapsack) would need more UI elements.
                // For this project, we'll keep it simple.
                break;
        }

        setControlsDisabled(true);
        try {
            const response = await fetch('/run_algorithm', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(params)
            });
            const result = await response.json();
            if (result.error) throw new Error(result.error);

            // Redraw initial state only if it's a data-driven algorithm
            if (algoInfo.ds !== 'conceptual') {
                 animator.drawInitialState(currentDataType, currentData);
            } else {
                 animator.clearAll(); // Clear board for conceptual animations
            }
           
            await animator.runAnimation(result.steps);
        } catch (error) {
            console.error("Algorithm execution failed:", error);
            animator.updateLog(`Execution Error: ${error.message}`);
        } finally {
            setControlsDisabled(false);
        }
    }

    // =================================================================
    // 5. ATTACH EVENT LISTENERS
    // =================================================================
    UI.dsSelect.addEventListener('change', handleDataStructureChange);
    UI.algoSelect.addEventListener('change', handleAlgorithmChange);
    UI.runBtn.addEventListener('click', runAlgorithm);
    document.getElementById('generate-random-array-btn').addEventListener('click', () => generateData(false));
    document.getElementById('generate-sorted-array-btn').addEventListener('click', () => generateData(true));
    document.getElementById('generate-tree-btn').addEventListener('click', () => generateData());
    document.getElementById('generate-graph-btn').addEventListener('click', () => generateData());

    // Tab functionality for info panel
    document.querySelectorAll('.tab-link').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelector('.tab-link.active')?.classList.remove('active');
            document.querySelector('.tab-content.active')?.classList.remove('active');
            button.classList.add('active');
            document.getElementById(button.dataset.tab).classList.add('active');
        });
    });

    // --- KICK OFF THE APPLICATION ---
    initialize();
});