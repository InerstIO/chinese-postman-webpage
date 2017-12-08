var cy = cytoscape({
    container: document.getElementById('cy'),

    boxSelectionEnabled: false,
    autounselectify: true,

    style: cytoscape.stylesheet()
        .selector('node')
        .css({
            'content': 'data(id)'
        })
        .selector('edge')
        .css({
            'curve-style': 'bezier',
            'width': 4,
            'line-color': '#ddd',
            'target-arrow-color': '#ddd',
            'label': 'data(weight)',
            'font-size': 8
        })
        .selector('.deledge')
        .css({
            'opacity': 0.3,
            'curve-style': 'bezier',
            'width': 4,
            'line-color': '#ddd',
            'line-style': 'dashed',
            'transition-property': 'opacity, line-style',
            'transition-duration': '2s'
        })
        .selector('.highlighted')
        .css({
            'opacity': 0.5,
            'display': 'element',
            'target-arrow-shape': 'triangle',
            'background-color': '#61bffc',
            'line-color': '#61bffc',
            'target-arrow-color': '#61bffc',
            'transition-property': 'background-color, line-color, target-arrow-color',
            'transition-duration': '1s'
        })
        .selector('.highlightednode')
        .css({
            'display': 'element',
            'target-arrow-shape': 'triangle',
            'background-color': '#61bffc',
            'line-color': '#61bffc',
            'target-arrow-color': '#61bffc',
            'transition-property': 'background-color, line-color, target-arrow-color',
            'transition-duration': '1s'
        })
        .selector('.nodeinpath')
        .css({
            'display': 'element',
            'border-color': '#61bffc',
            'border-opacity': 0.5,
            'border-width': 2,
            'border-style': 'dashed',
            'line-color': '#61bffc',
            'transition-property': 'border-color, border-width',
            'transition-duration': '0.1s'
        }),

    elements: {
        nodes: orinodes,

        edges: oriedges,
        },

    layout: {
        name: 'cose',
        directed: false,
        roots: '#1',
        padding: 10
    }
    });
    
    for (var i in nodeinpath) {
        nodesel = 'node[id="'+nodeinpath[i]+'"]';
        cy.elements(nodesel).addClass('nodeinpath');
    }

    for (var i in deledges) {
        edgesel = 'edge[source="'+deledges[i][0]+'"][target="'+deledges[i][1]+'"]';
        cy.elements(edgesel).addClass('deledge');
    }

    var highlightNode = function(i) {
        nodesel = 'node[id="'+i+'"]';
        cy.elements(nodesel).addClass('highlightednode');
    }

    var i = 0;
    if (path.length) {
        highlightNode(path[0][0]);
    }
    
    var highlightNextRoute = function() {
        if ( i < path.length) {
            setTimeout(highlightNode(path[i][1]), 1000);
            edgesel = 'edge[source="'+path[i][0]+'"][target="'+path[i][1]+'"]';
            revedgesel = 'edge[source="'+path[i][1]+'"][target="'+path[i][0]+'"]';
            if (cy.elements(edgesel).length) {
                weight = cy.elements(edgesel).data().weight;
            }else {
                weight = cy.elements(revedgesel).data().weight;
            }
            if (cy.elements(revedgesel).length && !cy.elements(revedgesel).hasClass('highlighted')) {
                cy.elements(revedgesel).remove();
                cy.add({data: { source: path[i][0], target: path[i][1], weight: weight }, classes: 'highlighted' });
            } else if (cy.elements(edgesel).length && !cy.elements(edgesel).hasClass('highlighted')) {
                cy.elements(edgesel).addClass('highlighted');
            } else {
                cy.add({data: { source: path[i][0], target: path[i][1], weight: weight }, classes: 'highlighted' });
            }
            i++;
            setTimeout(highlightNextRoute, 1000);
        }
    };

    setTimeout(highlightNextRoute, 2000);
