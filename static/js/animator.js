// static/js/animator.js

class Animator {
    constructor(containerId, auxContainerId, logId, speedSliderId) {
        this.container = document.getElementById(containerId);
        this.auxContainer = document.getElementById(auxContainerId);
        this.log = document.getElementById(logId);
        this.speedSlider = document.getElementById(speedSliderId);

        // State for complex visualizations
        this.dataType = null;
        this.nodeElements = {}; // For graph/tree SVG nodes
        this.linkElements = {}; // For graph/tree SVG edges
        this.treeData = {};     // For logical tree structure and coordinates
    }

    // =================================================================
    // 1. CORE ANIMATION & UTILITY METHODS
    // =================================================================

    getAnimationSpeed() {
        const max = parseInt(this.speedSlider.max);
        const min = parseInt(this.speedSlider.min);
        const value = parseInt(this.speedSlider.value);
        return (max + min) - value; // Invert slider for intuitive speed control
    }

    sleep() {
        return new Promise(resolve => setTimeout(resolve, this.getAnimationSpeed()));
    }

    updateLog(message) {
        this.log.innerHTML = `<p>${message}</p>`;
    }

    clearAll() {
        this.container.innerHTML = '';
        this.auxContainer.innerHTML = '';
        this.nodeElements = {};
        this.linkElements = {};
        this.treeData = {};
    }

    // =================================================================
    // 2. INITIAL STATE DRAWING
    // =================================================================

    drawInitialState(dataType, data) {
        this.clearAll();
        this.dataType = dataType;
        switch (dataType) {
            case 'array':
                this.drawArray(data);
                break;
            case 'graph':
                this.drawGraph(data);
                break;
            case 'tree':
                // Tree is built dynamically, start with an empty SVG canvas
                this.container.innerHTML = `<svg id="svg-vis" viewbox="0 0 800 400"></svg>`;
                break;
            // Other conceptual types might have specific initial drawing needs
        }
    }

    drawArray(data) {
        data.forEach((value, index) => {
            const element = document.createElement('div');
            element.classList.add('array-element');
            element.id = `el-${index}`;
            element.textContent = value;
            this.container.appendChild(element);
        });
    }

    drawGraph(graphData) {
        this.container.innerHTML = `<svg id="svg-vis" viewbox="0 0 700 400"></svg>`;
        const svg = this.container.querySelector('#svg-vis');
        const { nodes, adjacency_list } = graphData;

        // Draw links first (so they are behind nodes)
        for (const source in adjacency_list) {
            for (const target of adjacency_list[source]) {
                if (source < target) { // Avoid duplicate edges in undirected graphs
                    const linkId = `${source}-${target}`;
                    const sourceNode = nodes[source];
                    const targetNode = nodes[target];
                    const line = this.createSvgElement('line', { x1: sourceNode.x, y1: sourceNode.y, x2: targetNode.x, y2: targetNode.y, class: 'link' });
                    svg.appendChild(line);
                    this.linkElements[linkId] = line;
                    this.linkElements[`${target}-${source}`] = line;
                }
            }
        }
        
        // Draw nodes and labels
        for (const id in nodes) {
            const { x, y } = nodes[id];
            const group = this.createSvgElement('g', { class: 'node', id: `node-${id}` });
            const circle = this.createSvgElement('circle', { cx: x, cy: y, r: 20 });
            const text = this.createSvgElement('text', { x: x, y: y });
            text.textContent = id;
            
            group.appendChild(circle);
            group.appendChild(text);
            svg.appendChild(group);
            this.nodeElements[id] = group;
        }
    }

    // =================================================================
    // 3. BST (TREE) DRAWING LOGIC
    // =================================================================

    /**
     * Calculates the position for a new tree node and draws it.
     * @param {number} value - The value of the new node.
     * @param {number|null} parentValue - The value of the parent node.
     * @param {string} direction - 'left', 'right', or 'root'.
     */
    drawTreeNode(value, parentValue, direction) {
        const svg = this.container.querySelector('#svg-vis');
        if (!svg) return;

        let x, y, depth;
        const width = svg.clientWidth;
        const y_spacing = 60;
        const initial_x_offset = width / 4;

        if (direction === 'root') {
            depth = 0;
            x = width / 2;
            y = 50;
        } else {
            const parentNode = this.treeData[parentValue];
            if (!parentNode) return; // Should not happen
            depth = parentNode.depth + 1;
            const x_offset = initial_x_offset / Math.pow(2, depth - 1);
            x = (direction === 'left') ? parentNode.x - x_offset : parentNode.x + x_offset;
            y = parentNode.y + y_spacing;
        }

        // Store logical data and coordinates
        this.treeData[value] = { value, parent: parentValue, x, y, depth };

        // Draw link from parent
        if (parentValue !== null) {
            const parentNode = this.treeData[parentValue];
            const linkId = `${parentValue}-${value}`;
            const line = this.createSvgElement('line', { x1: parentNode.x, y1: parentNode.y, x2: x, y2: y, class: 'link' });
            svg.insertBefore(line, svg.firstChild); // Insert before nodes
            this.linkElements[linkId] = line;
        }

        // Draw node
        const group = this.createSvgElement('g', { class: 'node', id: `node-${value}` });
        const circle = this.createSvgElement('circle', { cx: x, cy: y, r: 20 });
        const text = this.createSvgElement('text', { x: x, y: y });
        text.textContent = value;

        group.appendChild(circle);
        group.appendChild(text);
        svg.appendChild(group);
        this.nodeElements[value] = group;
    }


    // =================================================================
    // 4. AUXILIARY & CUSTOM VISUALIZATION DRAWING
    // =================================================================

    drawAuxiliary(type, data) {
        this.auxContainer.innerHTML = '';
        if (!data || data.length === 0) return;

        const title = document.createElement('div');
        title.classList.add('aux-title');
        title.textContent = type.toUpperCase();
        this.auxContainer.appendChild(title);
        
        data.forEach(item => {
            const el = document.createElement('div');
            el.classList.add(`${type}-element`);
            el.textContent = item;
            this.auxContainer.appendChild(el);
        });
    }

    createSvgElement(tag, attrs) {
        const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
        for (const key in attrs) {
            el.setAttribute(key, attrs[key]);
        }
        return el;
    }
    
    // =================================================================
    // 5. THE MAIN ANIMATION LOOP
    // =================================================================

    async runAnimation(steps) {
        for (const step of steps) {
            // Reset transient highlights from the previous step
            document.querySelectorAll('.comparing, .min-element, .exploring, .visiting, .dp-highlight, .dp-referenced').forEach(el => 
                el.classList.remove('comparing', 'min-element', 'exploring', 'visiting', 'dp-highlight', 'dp-referenced')
            );
            
            this.updateLog(step.message);

            // --- Main Action Switch ---
            switch (step.action) {
                // --- Common Actions ---
                case 'error':
                    this.updateLog(`Error: ${step.message}`);
                    return;
                case 'complete':
                    // Final state, just log and finish
                    break;

                // --- Array Actions ---
                case 'compare':
                    step.indices.forEach(i => document.getElementById(`el-${i}`)?.classList.add('comparing'));
                    break;
                case 'swap':
                    const el1 = document.getElementById(`el-${step.indices[0]}`);
                    const el2 = document.getElementById(`el-${step.indices[1]}`);
                    if (el1 && el2) {
                        el1.classList.add('comparing');
                        el2.classList.add('comparing');
                        await this.sleep();
                        const tempText = el1.textContent;
                        el1.textContent = el2.textContent;
                        el2.textContent = tempText;
                    }
                    break;
                case 'found':
                    step.indices.forEach(i => document.getElementById(`el-${i}`)?.classList.add('found'));
                    await this.sleep();
                    return; // End animation
                case 'not_found':
                    // Just a message, handled by updateLog
                    break;
                case 'sorted_element':
                    step.indices.forEach(i => document.getElementById(`el-${i}`)?.classList.add('sorted'));
                    break;
                case 'highlight_min':
                    document.querySelectorAll('.min-element').forEach(el => el.classList.remove('min-element'));
                    step.indices.forEach(i => document.getElementById(`el-${i}`)?.classList.add('min-element'));
                    break;
                case 'eliminate': // For Binary Search
                    for (let i = step.range[0]; i <= step.range[1]; i++) {
                        document.getElementById(`el-${i}`)?.classList.add('faded');
                    }
                    break;

                // --- Graph & Traversal Actions ---
                case 'enqueue':
                case 'push':
                    this.drawAuxiliary(step.action === 'enqueue' ? 'queue' : 'stack', step.queue_state || step.stack_state);
                    this.nodeElements[step.node]?.classList.add('visiting');
                    break;
                case 'dequeue':
                case 'pop':
                    this.drawAuxiliary(step.action === 'dequeue' ? 'queue' : 'stack', step.queue_state || step.stack_state);
                    this.nodeElements[step.node]?.classList.add('visiting');
                    break;
                case 'visit_node':
                     this.nodeElements[step.node]?.classList.remove('visiting');
                     this.nodeElements[step.node]?.classList.add('visited');
                    break;
                case 'explore_edge':
                    const linkId = `${step.from}-${step.to}`;
                    this.linkElements[linkId]?.classList.add('exploring');
                    break;
                case 'neighbor_visited':
                case 'skip_visited':
                    this.nodeElements[step.node]?.classList.add('faded');
                    await this.sleep();
                    this.nodeElements[step.node]?.classList.remove('faded');
                    break;

                // --- Tree Actions (BST Build) ---
                case 'insert':
                    this.drawTreeNode(step.value, step.parent, step.direction);
                    this.nodeElements[step.value]?.classList.add('found'); // Briefly highlight new node
                    break;
                case 'traverse': // In tree context
                    const traverseLinkId = `${step.from}-${step.to}`;
                    this.linkElements[traverseLinkId]?.classList.add('exploring');
                    break;
                case 'compare': // In tree context
                     this.nodeElements[step.value]?.classList.add('comparing');
                     break;

                // --- DP Table Actions (Knapsack) ---
                case 'init_table':
                    // Code to draw the DP table structure
                    break;
                case 'highlight_cell':
                    document.getElementById(`cell-${step.cell[0]}-${step.cell[1]}`)?.classList.add('dp-highlight');
                    break;
                case 'copy_above':
                case 'compare_options':
                    // Code to highlight referenced cells
                    break;
            }
            await this.sleep();
        }
        this.updateLog("Animation complete.");
    }
}