// static/js/animator.js

class Animator {
    constructor(containerId, auxContainerId, logId, speedSliderId) {
        this.container = document.getElementById(containerId);
        this.auxContainer = document.getElementById(auxContainerId);
        this.log = document.getElementById(logId);
        this.speedSlider = document.getElementById(speedSliderId);

        // State for complex visualizations
        this.dataType = null;
        this.nodeElements = {};
        this.linkElements = {};
        this.distanceLabels = {};
        this.treeData = {};
    }

    // =================================================================
    // 1. CORE ANIMATION & UTILITY METHODS
    // =================================================================

    getAnimationSpeed() {
        const max = parseInt(this.speedSlider.max);
        const min = parseInt(this.speedSlider.min);
        const value = parseInt(this.speedSlider.value);
        return (max + min) - value;
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
        this.distanceLabels = {};
        this.treeData = {};
    }

    createSvgElement(tag, attrs) {
        const el = document.createElementNS('http://www.w3.org/2000/svg', tag);
        for (const key in attrs) {
            el.setAttribute(key, attrs[key]);
        }
        return el;
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
                this.container.innerHTML = `<svg id="svg-vis"></svg>`;
                break;
            // Conceptual algorithms may not need an initial drawing
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
        this.container.innerHTML = `<svg id="svg-vis"></svg>`;
        const svg = this.container.querySelector('#svg-vis');
        const { nodes, adjacency_list } = graphData;

        // Dynamically calculate viewBox to fit the graph
        const padding = 50;
        const coords = Object.values(nodes);
        const minX = Math.min(...coords.map(n => n.x));
        const maxX = Math.max(...coords.map(n => n.x));
        const minY = Math.min(...coords.map(n => n.y));
        const maxY = Math.max(...coords.map(n => n.y));
        svg.setAttribute('viewBox', `${minX - padding} ${minY - padding} ${maxX - minX + 2 * padding} ${maxY - minY + 2 * padding}`);

        const edgeGroup = this.createSvgElement('g'); // Group for edges
        const nodeGroup = this.createSvgElement('g'); // Group for nodes
        svg.appendChild(edgeGroup);
        svg.appendChild(nodeGroup);

        // Draw links and their weights
        for (const source in adjacency_list) {
            for (const neighbor of adjacency_list[source]) {
                const target = neighbor.node;
                const weight = neighbor.weight;
                if (source < target) {
                    const sourceNode = nodes[source];
                    const targetNode = nodes[target];
                    
                    const line = this.createSvgElement('line', { x1: sourceNode.x, y1: sourceNode.y, x2: targetNode.x, y2: targetNode.y, class: 'link' });
                    edgeGroup.appendChild(line);
                    this.linkElements[`${source}-${target}`] = this.linkElements[`${target}-${source}`] = line;

                    // Add weight label
                    const text = this.createSvgElement('text', {
                        x: (sourceNode.x + targetNode.x) / 2,
                        y: (sourceNode.y + targetNode.y) / 2 - 5,
                        class: 'link-weight'
                    });
                    text.textContent = weight;
                    edgeGroup.appendChild(text);
                }
            }
        }
        
        // Draw nodes, labels, and distance placeholders
        for (const id in nodes) {
            const { x, y } = nodes[id];
            const group = this.createSvgElement('g', { class: 'node', id: `node-${id}` });
            const circle = this.createSvgElement('circle', { cx: x, cy: y, r: 20 });
            const text = this.createSvgElement('text', { x: x, y: y });
            text.textContent = id;
            
            const distLabel = this.createSvgElement('text', { x: x, y: y + 32, class: 'distance-label' });
            distLabel.textContent = '∞';
            
            group.appendChild(circle);
            group.appendChild(text);
            group.appendChild(distLabel);
            nodeGroup.appendChild(group);
            this.nodeElements[id] = group;
            this.distanceLabels[id] = distLabel;
        }
    }

    // =================================================================
    // 3. SPECIALIZED DRAWING (BST, DP TABLE)
    // =================================================================

    drawTreeNode(value, parentValue, direction) {
        const svg = this.container.querySelector('#svg-vis');
        if (!svg) return;
        
        if (!svg.viewBox.baseVal.width) {
             svg.setAttribute('viewBox', `0 0 ${this.container.clientWidth} ${this.container.clientHeight}`);
        }

        let x, y, depth;
        const width = svg.viewBox.baseVal.width;
        const y_spacing = 60;
        const initial_x_offset = width / 4;

        if (direction === 'root') {
            depth = 0;
            x = width / 2;
            y = 50;
        } else {
            const parentNode = this.treeData[parentValue];
            if (!parentNode) return;
            depth = parentNode.depth + 1;
            const x_offset = initial_x_offset / Math.pow(1.8, depth); // Fine-tuned offset
            x = (direction === 'left') ? parentNode.x - x_offset : parentNode.x + x_offset;
            y = parentNode.y + y_spacing;
        }

        this.treeData[value] = { value, parent: parentValue, x, y, depth };

        if (parentValue !== null) {
            const parentNode = this.treeData[parentValue];
            const linkId = `${parentValue}-${value}`;
            const line = this.createSvgElement('line', { x1: parentNode.x, y1: parentNode.y, x2: x, y2: y, class: 'link' });
            svg.insertBefore(line, svg.firstChild);
            this.linkElements[linkId] = line;
        }

        const group = this.createSvgElement('g', { class: 'node', id: `node-${value}` });
        const circle = this.createSvgElement('circle', { cx: x, cy: y, r: 20 });
        const text = this.createSvgElement('text', { x: x, y: y });
        text.textContent = value;

        group.appendChild(circle);
        group.appendChild(text);
        svg.appendChild(group);
        this.nodeElements[value] = group;
    }

    drawDPTable(rows, cols, weights, values) {
        this.auxContainer.innerHTML = '';
        const table = document.createElement('table');
        table.classList.add('dp-table');
        
        // Header Row
        const thead = table.createTHead();
        const headerRow = thead.insertRow();
        headerRow.insertCell().textContent = 'Item';
        headerRow.insertCell().textContent = 'W/V';
        for (let w = 0; w < cols; w++) {
            headerRow.insertCell().textContent = w;
        }

        // Body Rows
        const tbody = table.createTBody();
        for (let i = 0; i < rows; i++) {
            const row = tbody.insertRow();
            if (i > 0) {
                row.insertCell().textContent = `i=${i}`;
                row.insertCell().textContent = `${weights[i-1]}/${values[i-1]}`;
            } else {
                row.insertCell().textContent = 'i=0';
                row.insertCell().textContent = '-';
            }
            for (let w = 0; w < cols; w++) {
                const cell = row.insertCell();
                cell.id = `cell-${i}-${w}`;
                cell.textContent = '0';
            }
        }
        this.auxContainer.appendChild(table);
    }

    // =================================================================
    // 4. THE MAIN ANIMATION LOOP
    // =================================================================

    async runAnimation(steps) {
        for (const step of steps) {
            // Reset transient highlights from previous step
            document.querySelectorAll('.comparing, .min-element, .exploring, .visiting, .dp-highlight, .dp-referenced, .updated, .faded')
                .forEach(el => el.classList.remove('comparing', 'min-element', 'exploring', 'visiting', 'dp-highlight', 'dp-referenced', 'updated', 'faded'));
            
            this.updateLog(step.message);

            // --- Main Action Switch ---
            switch (step.action) {
                // Common Actions
                case 'error': this.updateLog(`Error: ${step.message}`); return;
                case 'complete': break;

                // Array Actions
                case 'compare': step.indices.forEach(i => document.getElementById(`el-${i}`)?.classList.add('comparing')); break;
                case 'swap':
                    const el1 = document.getElementById(`el-${step.indices[0]}`);
                    const el2 = document.getElementById(`el-${step.indices[1]}`);
                    if (el1 && el2) {
                        el1.classList.add('comparing'); el2.classList.add('comparing');
                        await this.sleep();
                        [el1.textContent, el2.textContent] = [el2.textContent, el1.textContent];
                    }
                    break;
                case 'found': step.indices.forEach(i => document.getElementById(`el-${i}`)?.classList.add('found')); await this.sleep(); return;
                case 'sorted_element': step.indices.forEach(i => document.getElementById(`el-${i}`)?.classList.add('sorted')); break;
                case 'highlight_min': step.indices.forEach(i => document.getElementById(`el-${i}`)?.classList.add('min-element')); break;
                case 'eliminate': for (let i = step.range[0]; i <= step.range[1]; i++) { document.getElementById(`el-${i}`)?.classList.add('faded'); } break;
                
                // Graph & Traversal Actions
                case 'enqueue': case 'push': this.drawAuxiliary(step.action === 'enqueue' ? 'queue' : 'stack', step.queue_state || step.stack_state); this.nodeElements[step.node]?.classList.add('visiting'); break;
                case 'dequeue': case 'pop': this.drawAuxiliary(step.action === 'dequeue' ? 'queue' : 'stack', step.queue_state || step.stack_state); this.nodeElements[step.node]?.classList.add('visiting'); break;
                case 'visit_node': this.nodeElements[step.node]?.classList.remove('visiting'); this.nodeElements[step.node]?.classList.add('visited'); break;
                case 'explore_edge': this.linkElements[`${step.from}-${step.to}`]?.classList.add('exploring'); break;
                case 'neighbor_visited': case 'skip_visited': this.nodeElements[step.node]?.classList.add('faded'); break;

                // Tree Actions (BST Build)
                case 'insert': this.drawTreeNode(step.value, step.parent, step.direction); this.nodeElements[step.value]?.classList.add('found'); break;
                case 'traverse': this.nodeElements[step.from]?.classList.add('comparing'); break;
                
                // Dijkstra Actions
                case 'init_distances': Object.keys(step.distances).forEach(node => this.distanceLabels[node].textContent = step.distances[node] === Infinity ? '∞' : step.distances[node]); break;
                case 'update_distance': this.distanceLabels[step.node].textContent = step.new_dist; this.distanceLabels[step.node].classList.add('updated'); this.nodeElements[step.node]?.classList.add('visiting'); break;
                case 'highlight_path':
                    for (let i = 0; i < step.path.length - 1; i++) {
                        this.nodeElements[step.path[i]]?.classList.add('path-node');
                        this.linkElements[`${step.path[i]}-${step.path[i+1]}`]?.classList.add('path-link');
                    }
                    this.nodeElements[step.path.at(-1)]?.classList.add('path-node');
                    break;

                // Knapsack (DP) Actions
                case 'init_table': this.drawDPTable(step.rows, step.cols, step.weights, step.values); break;
                case 'highlight_cell': document.getElementById(`cell-${step.cell[0]}-${step.cell[1]}`)?.classList.add('dp-highlight'); break;
                case 'copy_above':
                    const fromCell = document.getElementById(`cell-${step.from_cell[0]}-${step.from_cell[1]}`);
                    const toCell = document.getElementById(`cell-${step.to_cell[0]}-${step.to_cell[1]}`);
                    fromCell?.classList.add('dp-referenced');
                    if (toCell) toCell.textContent = step.value;
                    break;
                case 'compare_options':
                    const withoutCell = document.getElementById(`cell-${step.option_without.cell[0]}-${step.option_without.cell[1]}`);
                    const withCell = document.getElementById(`cell-${step.option_with.cell[0]}-${step.option_with.cell[1]}`);
                    const resultCell = document.getElementById(`cell-${step.cell[0]}-${step.cell[1]}`);
                    withoutCell?.classList.add('dp-referenced');
                    withCell?.classList.add('dp-referenced');
                    if (resultCell) resultCell.textContent = step.result;
                    break;
            }
            await this.sleep();
        }
        this.updateLog("Animation complete.");
    }
}