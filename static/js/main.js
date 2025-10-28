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
    // Using a single object to hold references for cleaner code
    const UI = {
        dsSelect: document.getElementById('ds-select'),
        algoSelect: document.getElementById('algo-select'),
        dataSizeInput: document.getElementById('data-size'),
        runBtn: document.getElementById('run-btn'),
        generationControls: document.getElementById('generation-controls'),
        executionInputs: document.getElementById('execution-inputs'),
        targetInputGroup: document.getElementById('target-input-group'),
        startNodeGroup: document.getElementById('start-node-group'),
        startNodeSelect: document.getElementById('start-node-select'),
        targetValueInput: document.getElementById('target-value'),
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
     * Kicks off the application by fetching content and setting up the initial UI state.
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
    // 2. UI UPDATE & MANAGEMENT FUNCTIONS
    // =================================================================

    function populateDataStructureSelect() {
        UI.dsSelect.innerHTML = '';
        Object.keys(ALL_CONTENT.data_structures).forEach(dsKey => {
            // We only add options for data structures that have associated visualizable algorithms.
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
        UI.algoSelect.innerHTML = ''; // Clear previous options
        
        Object.keys(ALL_CONTENT.algorithms).forEach(key => {
            const algo = ALL_CONTENT.algorithms[key];
            // Filter algorithms to match the selected data structure
            if (algo.ds === selectedDs) {
                const option = document.createElement('option');
                option.value = key;
                option.textContent = algo.name;
                UI.algoSelect.appendChild(option);
            }
        });
        handleAlgorithmChange(); // Update other UI elements based on the new selection
    }

    function updateGenerationControls() {
        // Hide all generation buttons
        UI.generationControls.querySelectorAll('button').forEach(btn => btn.style.display = 'none');
        
        // Show only the buttons relevant to the selected data structure
        switch (currentDataType) {
            case 'array':
                document.getElementById('generate-random-array-btn').style.display = 'block';
                document.getElementById('generate-sorted-array-btn').style.display = 'block';
                break;
            case 'tree':
                document.getElementById('generate-tree-btn').style.display = 'block';
                break;
            case 'graph':
                document.getElementById('generate-graph-btn').style.display = 'block';
                break;
        }
    }

    function updateExecutionInputs() {
        const algoKey = UI.algoSelect.value;
        const algoCategory = ALL_CONTENT.algorithms[algoKey]?.category;

        // Hide all contextual input fields
        UI.targetInputGroup.style.display = 'none';
        UI.startNodeGroup.style.display = 'none';
        
        // Show inputs based on the algorithm's category
        if (algoCategory === 'Searching') {
            UI.targetInputGroup.style.display = 'block';
        } else if (['Graph Traversal', 'Shortest Path'].includes(algoCategory)) {
            UI.startNodeGroup.style.display = 'block';
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
    // 3. EVENT HANDLERS
    // =================================================================

    function handleDataStructureChange() {
        currentDataType = UI.dsSelect.value;
        populateAlgoSelect();
        updateGenerationControls();
        generateData(); // Automatically generate new data when the type changes
    }

    function handleAlgorithmChange() {
        updateExecutionInputs();
        updateInfoPanel();
    }
    
    // =================================================================
    // 4. CORE LOGIC (API COMMUNICATION & ORCHESTRATION)
    // =================================================================

    async function generateData(isSorted = false) {
        setControlsDisabled(true);
        animator.updateLog(`Generating ${currentDataType}...`);
        try {
            const response = await fetch('/generate_data', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify({ size: UI.dataSizeInput.value, dtype: currentDataType, sorted: isSorted })
            });
            currentData = await response.json();
            
            animator.drawInitialState(currentDataType, currentData);
            animator.updateLog("New data generated. Ready to run an algorithm.");

            // If it's a graph, populate the start node selector
            if (currentDataType === 'graph' && currentData.nodes) {
                UI.startNodeSelect.innerHTML = '';
                Object.keys(currentData.nodes).sort().forEach(nodeId => {
                    const option = document.createElement('option');
                    option.value = nodeId;
                    option.textContent = `Node ${nodeId}`;
                    UI.startNodeSelect.appendChild(option);
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
        if (!currentData) {
            animator.updateLog("Please generate data first.");
            return;
        }

        const params = {
            algorithm: algoKey,
            input_data: currentData
        };
        const algoCategory = ALL_CONTENT.algorithms[algoKey]?.category;
        
        // Add specific parameters based on algorithm type
        if (algoCategory === 'Searching') {
            if (!UI.targetValueInput.value) {
                animator.updateLog("Please enter a target value to search for.");
                return;
            }
            params.target = UI.targetValueInput.value;
        }
        if (['Graph Traversal', 'Shortest Path'].includes(algoCategory)) {
            params.start_node = UI.startNodeSelect.value;
        }

        setControlsDisabled(true);
        try {
            const response = await fetch('/run_algorithm', {
                method: 'POST',
                headers: {'Content-Type': 'application/json'},
                body: JSON.stringify(params)
            });
            const result = await response.json();
            
            if (result.error) throw new Error(result.error);
            
            // Redraw initial state to reset visuals before starting the new animation
            animator.drawInitialState(currentDataType, currentData);
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

    // Generation buttons
    document.getElementById('generate-random-array-btn').addEventListener('click', () => generateData(false));
    document.getElementById('generate-sorted-array-btn').addEventListener('click', () => generateData(true));
    document.getElementById('generate-tree-btn').addEventListener('click', () => generateData());
    document.getElementById('generate-graph-btn').addEventListener('click', () => generateData());

    // Tab functionality for info panel
    document.querySelectorAll('.tab-link').forEach(button => {
        button.addEventListener('click', () => {
            document.querySelector('.tab-link.active').classList.remove('active');
            document.querySelector('.tab-content.active').classList.remove('active');
            button.classList.add('active');
            document.getElementById(button.dataset.tab).classList.add('active');
        });
    });

    // --- KICK OFF THE APPLICATION ---
    initialize();
});