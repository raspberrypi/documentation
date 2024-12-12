/* Trigger Tocbot dynamic TOC, works with tocbot 3.0.2 */
function makeToc() {
    var tocElement = document.getElementById('toc');
    if (tocElement) { /* only run on pages that have a toc -- exclude boxes landing pages, for instance */
        var oldtoc = tocElement.nextElementSibling;
        var newtoc = document.getElementById('tocbot');
        newtoc.setAttribute('id', 'tocbot');
        newtoc.setAttribute('class', 'js-toc');
        oldtoc.parentNode.replaceChild(newtoc, oldtoc);
        tocbot.init({ contentSelector: '#content',
            headingSelector: 'h1, h2, h3, h4',
            smoothScroll: true,
            includeHtml: true
        });
        var handleTocOnResize = function() {
            var width = window.innerWidth
                        || document.documentElement.clientWidth
                        || document.body.clientWidth;
            if (width < 768) {
                tocbot.refresh({ contentSelector: '#content',
                    headingSelector: 'h1, h2, h3, h4',
                    collapseDepth: 6,
                    activeLinkClass: 'ignoreactive',
                    throttleTimeout: 1000,
                    smoothScroll: true });
            }
            else {
                tocbot.refresh({ contentSelector: '#content',
                    headingSelector: 'h1, h2, h3, h4',
                    smoothScroll: true });
            }
        };
        window.addEventListener('resize', handleTocOnResize);
        handleTocOnResize();
    }
}

var currentParentID;
var currentParentInputID;
var currentChildID;

function initialiseCurrentToc(parentID, parentInputID = null, childID = null) {
    // highlight the new parent
    var newParent = document.getElementById(parentID);
    newParent.setAttribute('style', 'font-weight:bold');
    currentParentID = parentID;

    // if a parent input id is specified, expand the parent element
    if (parentInputID) {
        var newParentInput = document.getElementById(parentInputID);
        newParentInput.click();
        currentParentInputID = parentInputID;
    }

    // if a child is specified, highlight the child
    if (childID) {
        var newChild = document.getElementById(childID);
        newChild.setAttribute('style', 'font-weight:bold');
        currentChildID = childID;
    }
}

function updateCurrentToc(parentID, parentInputID = null, childID = null) {
    if (currentParentID == null && currentChildID == null) {
        initialiseCurrentToc(parentID, parentInputID, childID)
    } else {
        // if a parent input id is specified, but no child, expand the parent element
        // why no child? because if someone clicks the child within a parent, they don't want the parent section to collapse!
        if (parentInputID && childID == null) {
            var newParentInput = document.getElementById(parentInputID);
            newParentInput.click();
            currentParentInputID = parentInputID;
        }

        // if this is a new parent id, de-highlight the old parent and highlight the new one
        if (currentParentID != parentID) {
            var oldParent = document.getElementById(currentParentID);
            oldParent.style.removeProperty('font-weight');
            var newParent = document.getElementById(parentID);
            newParent.setAttribute('style', 'font-weight:bold');
            currentParentID = parentID;
        }

        // if there is an old child highlighted, un-highlight it
        if (currentChildID) {
            var oldChild = document.getElementById(currentChildID);
            oldChild.style.removeProperty('font-weight');
        }

        // if there is a new child, highlight it
        if (childID != null) {
            var newChild = document.getElementById(childID);

            newChild.setAttribute('style', 'font-weight:bold');
        }
        currentChildID = childID;
    }
}